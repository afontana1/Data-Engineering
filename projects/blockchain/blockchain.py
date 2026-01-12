from __future__ import annotations

import abc
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Protocol, Tuple


# ============================================================
# Domain objects (transactions, blocks)
# ============================================================

@dataclass(frozen=True)
class Transaction:
    """
    A minimal transaction type.

    This intentionally models the "methods" layer at a high level: an input that
    the state transition function can validate and apply to a state.

    In a real chain (e.g., Ethereum), transactions contain signatures, nonces,
    fee rules, gas, and more. Here we model only a token transfer intent.

    Attributes
    ----------
    sender:
        Account/address sending value.
    recipient:
        Account/address receiving value.
    amount:
        Amount of tokens to transfer.
    nonce:
        A per-sender monotonic number to prevent replay and enforce ordering.
    """
    sender: str
    recipient: str
    amount: int
    nonce: int


@dataclass(frozen=True)
class BlockHeader:
    """
    Minimal block header.

    Attributes
    ----------
    parent_hash:
        Hash of the parent block (defines ordering / chain).
    timestamp:
        UNIX timestamp (seconds).
    proposer_id:
        Identifier of the node/validator that proposed the block.
    """
    parent_hash: str
    timestamp: float
    proposer_id: str


@dataclass(frozen=True)
class Block:
    """
    A block: header + ordered list of transactions.

    In many real systems, a block also includes receipts, commitments (e.g. state
    root), signatures, and consensus-specific fields. Here we keep the minimum.

    Attributes
    ----------
    header:
        Metadata including parent link and proposer.
    transactions:
        Ordered list of transactions to apply.
    signature:
        A toy "signature" field used by PoA consensus to authenticate proposer.
        We treat it as a string computed by the proposer and checked by consensus.
    """
    header: BlockHeader
    transactions: Tuple[Transaction, ...]
    signature: str

    def block_hash(self) -> str:
        """
        Compute a deterministic hash for the block.

        Notes
        -----
        This is not meant to be cryptographically production-grade. It's a stable,
        deterministic identifier in this toy model.
        """
        payload = {
            "parent_hash": self.header.parent_hash,
            "timestamp": self.header.timestamp,
            "proposer_id": self.header.proposer_id,
            "transactions": [tx.__dict__ for tx in self.transactions],
            "signature": self.signature,
        }
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


# ============================================================
# Interfaces (SOLID: depend on abstractions)
# ============================================================

class StateStore(abc.ABC):
    """
    Interface: a store for the canonical state.

    In your generalized definition this is the "ledger" / state data structure.
    For Ethereum it's the EVM state; for UTXO chains it's the UTXO set.

    A StateStore should support:
    - reading values,
    - applying state updates (usually via transition function),
    - copying/forking state (useful for validation).
    """

    @abc.abstractmethod
    def get(self, key: str) -> int:
        """Return the integer value for a key, defaulting to 0 if absent."""

    @abc.abstractmethod
    def set(self, key: str, value: int) -> None:
        """Set a key to an integer value."""

    @abc.abstractmethod
    def snapshot(self) -> "StateStore":
        """
        Return an independent copy of the state.

        Consensus and validation often require simulating a block before accepting it.
        """


class StateTransitionFunction(abc.ABC):
    """
    Interface: the "methods" / state transition rules.

    Given a prior state and an input (transaction or block), this component:
    - validates whether the transition is legal
    - applies the transition to produce a new state

    In Ethereum this corresponds to protocol rules + EVM execution semantics.
    """

    @abc.abstractmethod
    def validate_transaction(self, state: StateStore, tx: Transaction) -> None:
        """
        Validate a transaction against the provided state.

        Raises
        ------
        ValueError
            If the transaction is invalid (insufficient funds, bad nonce, etc.).
        """

    @abc.abstractmethod
    def apply_transaction(self, state: StateStore, tx: Transaction) -> None:
        """
        Apply a transaction to the provided state.

        Contract
        --------
        Implementations should assume `validate_transaction` has already passed,
        or re-check invariants defensively.
        """


class ConsensusProtocol(abc.ABC):
    """
    Interface: consensus mechanism for selecting a canonical block sequence.

    This corresponds to:
    - proposer selection / sybil resistance (PoW, PoS, PoA, etc.)
    - block validity rules (e.g., signatures, difficulty)
    - fork choice (how nodes decide which chain head to follow)

    In this toy model we keep it intentionally minimal:
    - verify block eligibility (auth / signature / parent linkage)
    - choose the "best" head among competing tips
    """

    @abc.abstractmethod
    def verify_block(self, block: Block, known_parent_hashes: Iterable[str]) -> None:
        """
        Validate block eligibility / consensus-level rules.

        Parameters
        ----------
        block:
            The candidate block.
        known_parent_hashes:
            Hashes of blocks the node already knows (used to ensure parent exists).

        Raises
        ------
        ValueError
            If the block violates consensus rules.
        """

    @abc.abstractmethod
    def select_head(self, tips: List[str], height_by_hash: Dict[str, int]) -> str:
        """
        Choose the canonical head given multiple candidate tips.

        Parameters
        ----------
        tips:
            List of candidate chain tip hashes.
        height_by_hash:
            A mapping from block hash to chain height.

        Returns
        -------
        str
            The selected canonical head hash.
        """


# ============================================================
# Concrete implementations
# ============================================================

class KeyValueState(StateStore):
    """
    A simple key->int state store.

    We use keys for:
    - balances: "bal:<address>"
    - nonces:   "nonce:<address>"

    This is a toy version of an account-based ledger.

    Notes
    -----
    This class is deliberately small: it stores data and supports snapshots.
    It does NOT decide what is valid — that's the transition function's job.
    """

    def __init__(self, data: Optional[Dict[str, int]] = None) -> None:
        self._data: Dict[str, int] = dict(data) if data else {}

    def get(self, key: str) -> int:
        return self._data.get(key, 0)

    def set(self, key: str, value: int) -> None:
        self._data[key] = int(value)

    def snapshot(self) -> "KeyValueState":
        return KeyValueState(self._data)

    def dump(self) -> Dict[str, int]:
        """
        Return a copy of internal data for debugging / display.

        In real systems, direct dumping isn't always available or safe,
        but it's useful in a toy model.
        """
        return dict(self._data)


class TokenTransferTransition(StateTransitionFunction):
    """
    A state transition function implementing token transfers.

    Rules enforced
    --------------
    - amount must be positive
    - sender must have enough balance
    - nonce must match expected sender nonce
    - balances and nonces are updated deterministically

    This models the "legal changes to the data structure."
    """

    BAL_PREFIX = "bal:"
    NONCE_PREFIX = "nonce:"

    def _bal_key(self, addr: str) -> str:
        return f"{self.BAL_PREFIX}{addr}"

    def _nonce_key(self, addr: str) -> str:
        return f"{self.NONCE_PREFIX}{addr}"

    def validate_transaction(self, state: StateStore, tx: Transaction) -> None:
        if tx.amount <= 0:
            raise ValueError("Amount must be positive.")

        sender_bal = state.get(self._bal_key(tx.sender))
        if sender_bal < tx.amount:
            raise ValueError("Insufficient funds.")

        expected_nonce = state.get(self._nonce_key(tx.sender))
        if tx.nonce != expected_nonce:
            raise ValueError(f"Bad nonce. Expected {expected_nonce}, got {tx.nonce}.")

        # Optional sanity: allow self-transfer but it's usually pointless.
        if not tx.sender or not tx.recipient:
            raise ValueError("Sender and recipient must be non-empty strings.")

    def apply_transaction(self, state: StateStore, tx: Transaction) -> None:
        # Defensive: validate again for safety in this toy model.
        self.validate_transaction(state, tx)

        sender_key = self._bal_key(tx.sender)
        recipient_key = self._bal_key(tx.recipient)
        nonce_key = self._nonce_key(tx.sender)

        state.set(sender_key, state.get(sender_key) - tx.amount)
        state.set(recipient_key, state.get(recipient_key) + tx.amount)
        state.set(nonce_key, state.get(nonce_key) + 1)


class ProofOfAuthorityConsensus(ConsensusProtocol):
    """
    A very simple Proof-of-Authority (PoA) consensus.

    Overview
    --------
    - A fixed set of authorized proposers exist (validator IDs).
    - Each proposer has a shared secret used to create a toy signature.
    - A block is valid if:
        1) its parent exists (or it's a genesis child depending on setup)
        2) proposer is authorized
        3) signature matches the proposer secret and block header content

    Fork choice
    -----------
    - Choose the highest height (longest chain).
    - Tie-break by lexicographic hash.

    Notes
    -----
    This is NOT secure cryptography and is not meant for production use.
    It's a compact example of how consensus can be abstracted and injected.
    """

    def __init__(self, proposer_secrets: Dict[str, str]) -> None:
        """
        Parameters
        ----------
        proposer_secrets:
            Mapping proposer_id -> shared secret string.
        """
        self._secrets = dict(proposer_secrets)

    def _expected_signature(self, header: BlockHeader) -> str:
        secret = self._secrets[header.proposer_id]
        msg = f"{header.parent_hash}|{header.timestamp}|{header.proposer_id}"
        raw = (msg + "|" + secret).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def verify_block(self, block: Block, known_parent_hashes: Iterable[str]) -> None:
        if block.header.proposer_id not in self._secrets:
            raise ValueError("Unauthorized proposer.")

        if block.header.parent_hash not in set(known_parent_hashes):
            raise ValueError("Unknown parent; cannot attach block.")

        expected_sig = self._expected_signature(block.header)
        if block.signature != expected_sig:
            raise ValueError("Invalid proposer signature.")

        # Optional consensus-level checks
        if block.header.timestamp <= 0:
            raise ValueError("Invalid timestamp.")

    def select_head(self, tips: List[str], height_by_hash: Dict[str, int]) -> str:
        if not tips:
            raise ValueError("No tips to select from.")

        # Longest chain, deterministic tie-break.
        tips_sorted = sorted(
            tips,
            key=lambda h: (height_by_hash.get(h, -1), h),
            reverse=True,
        )
        return tips_sorted[0]


# ============================================================
# Node, mempool, and network
# ============================================================

class Mempool:
    """
    A simple transaction pool.

    In real networks, mempools include fee prioritization, eviction, anti-spam
    heuristics, and gossip de-duplication. Here we keep it as FIFO.
    """

    def __init__(self) -> None:
        self._txs: List[Transaction] = []

    def add(self, tx: Transaction) -> None:
        self._txs.append(tx)

    def drain(self, max_count: int) -> List[Transaction]:
        picked = self._txs[:max_count]
        self._txs = self._txs[max_count:]
        return picked

    def __len__(self) -> int:
        return len(self._txs)


@dataclass
class ChainIndex:
    """
    Minimal chain index tracking blocks, parents, and heights.

    This is kept separate from Node's other concerns (SRP).
    """
    blocks_by_hash: Dict[str, Block] = field(default_factory=dict)
    parent_by_hash: Dict[str, str] = field(default_factory=dict)
    height_by_hash: Dict[str, int] = field(default_factory=dict)
    tips: List[str] = field(default_factory=list)

    def add_block(self, block: Block) -> None:
        h = block.block_hash()
        self.blocks_by_hash[h] = block
        self.parent_by_hash[h] = block.header.parent_hash
        self.height_by_hash[h] = self.height_by_hash.get(block.header.parent_hash, 0) + 1

        # Update tips: remove parent if it was a tip, add new tip.
        if block.header.parent_hash in self.tips:
            self.tips.remove(block.header.parent_hash)
        if h not in self.tips:
            self.tips.append(h)

    def known_hashes(self) -> Iterable[str]:
        return self.blocks_by_hash.keys()


class Node:
    """
    A full node that:
    - receives transactions and blocks
    - validates blocks using consensus + state transition rules
    - maintains a local canonical head and state

    Key SOLID point: Node depends on abstractions:
    - StateStore
    - StateTransitionFunction
    - ConsensusProtocol

    So you can swap in:
    - UTXO state store
    - EVM-like transition function
    - PoW / PoS consensus
    without rewriting Node.
    """

    def __init__(
        self,
        node_id: str,
        state: StateStore,
        transition: StateTransitionFunction,
        consensus: ConsensusProtocol,
        mempool: Optional[Mempool] = None,
    ) -> None:
        self.node_id = node_id
        self.state = state
        self.transition = transition
        self.consensus = consensus
        self.mempool = mempool or Mempool()

        self.chain = ChainIndex()
        self.head_hash: Optional[str] = None

    # ----------------------------
    # Genesis / initialization
    # ----------------------------

    def init_genesis(self, genesis_state: Dict[str, int]) -> None:
        """
        Initialize the node with a genesis block and a preloaded state.

        Parameters
        ----------
        genesis_state:
            Initial key->int values for the state store. In this toy model this
            should include balances/nonces keys.
        """
        # Load genesis state
        for k, v in genesis_state.items():
            self.state.set(k, v)

        # Create a genesis block that is treated as "already known."
        genesis_header = BlockHeader(parent_hash="GENESIS", timestamp=0.0, proposer_id="GENESIS")
        genesis_block = Block(header=genesis_header, transactions=tuple(), signature="GENESIS")
        genesis_hash = genesis_block.block_hash()

        # Insert genesis directly; allow it to have a dummy parent hash.
        self.chain.blocks_by_hash[genesis_hash] = genesis_block
        self.chain.parent_by_hash[genesis_hash] = "GENESIS"
        self.chain.height_by_hash[genesis_hash] = 0
        self.chain.tips = [genesis_hash]
        self.head_hash = genesis_hash

    # ----------------------------
    # Receiving transactions/blocks
    # ----------------------------

    def receive_transaction(self, tx: Transaction) -> None:
        """
        Receive a transaction into the mempool.

        This is similar to how lightweight clients or peers gossip transactions.
        """
        # Validate against current canonical state (like mempool admission rules).
        self.transition.validate_transaction(self.state, tx)
        self.mempool.add(tx)

    def receive_block(self, block: Block) -> None:
        """
        Receive a candidate block and attempt to accept it.

        Validation steps
        ----------------
        1) Consensus-level verification (proposer eligibility + parent known)
        2) Execute transactions against a snapshot to ensure deterministic validity
        3) If valid, add to chain index and update canonical head via fork choice
        4) If head changes, rebuild canonical state

        Notes
        -----
        In real clients, state rebuild is optimized with incremental updates and
        persistent databases. Here we rebuild for clarity.
        """
        # 1) Consensus-level checks
        self.consensus.verify_block(block, known_parent_hashes=self.chain.known_hashes())

        # 2) Execute on a snapshot to validate all transitions
        test_state = self.state.snapshot()
        for tx in block.transactions:
            self.transition.validate_transaction(test_state, tx)
            self.transition.apply_transaction(test_state, tx)

        # 3) Add to chain
        self.chain.add_block(block)

        # 4) Fork choice: select canonical head and rebuild state if changed
        new_head = self.consensus.select_head(self.chain.tips, self.chain.height_by_hash)
        if new_head != self.head_hash:
            self.head_hash = new_head
            self._rebuild_state_from_genesis_to_head()

    # ----------------------------
    # Proposing blocks
    # ----------------------------

    def propose_block(self, proposer_secret: str, max_txs: int = 100) -> Block:
        """
        Create a new block extending the current head.

        Parameters
        ----------
        proposer_secret:
            Secret used by PoA consensus to build a toy signature.
            (In real systems this would be a private key signature.)
        max_txs:
            Max transactions to include from mempool.

        Returns
        -------
        Block
            The proposed block. It is not automatically broadcast.

        Raises
        ------
        ValueError
            If the node is not initialized (no head).
        """
        if self.head_hash is None:
            raise ValueError("Node not initialized; call init_genesis first.")

        txs = tuple(self.mempool.drain(max_txs))
        header = BlockHeader(
            parent_hash=self.head_hash,
            timestamp=time.time(),
            proposer_id=self.node_id,
        )

        # Signature scheme compatible with ProofOfAuthorityConsensus
        msg = f"{header.parent_hash}|{header.timestamp}|{header.proposer_id}"
        signature = hashlib.sha256((msg + "|" + proposer_secret).encode("utf-8")).hexdigest()

        return Block(header=header, transactions=txs, signature=signature)

    # ----------------------------
    # Helpers
    # ----------------------------

    def _path_to_genesis(self, head_hash: str) -> List[str]:
        """
        Return the chain of block hashes from genesis->head (inclusive).

        Assumes genesis is the only block with height 0 in this toy model.
        """
        path = []
        cur = head_hash
        while True:
            path.append(cur)
            parent = self.chain.parent_by_hash[cur]
            if self.chain.height_by_hash[cur] == 0:
                break
            cur = parent
        return list(reversed(path))

    def _rebuild_state_from_genesis_to_head(self) -> None:
        """
        Rebuild canonical state by replaying blocks from genesis to current head.

        This is slow but very clear. Real clients maintain incremental state and
        database snapshots.
        """
        if self.head_hash is None:
            return

        # Find genesis state by copying current state's *genesis-loaded* data.
        # To keep things simple, we assume init_genesis loaded the initial state.
        # We'll rebuild by:
        # - snapshot current state
        # - reset to genesis snapshot
        # - replay blocks excluding genesis block itself.
        genesis_snapshot = self.state.snapshot()

        # Reset state store to genesis snapshot by replacing internal data if possible.
        # Since StateStore is abstract, we do it generically by "reloading" keys:
        # This toy version relies on KeyValueState.dump for demonstration.
        if isinstance(genesis_snapshot, KeyValueState) and isinstance(self.state, KeyValueState):
            self.state = KeyValueState(genesis_snapshot.dump())
        else:
            # Fallback: we can't generically enumerate all keys from StateStore,
            # so real implementations would need a richer StateStore interface.
            raise RuntimeError("StateStore implementation does not support rebuild in this toy model.")

        path = self._path_to_genesis(self.head_hash)
        for h in path[1:]:  # skip genesis
            blk = self.chain.blocks_by_hash[h]
            for tx in blk.transactions:
                self.transition.apply_transaction(self.state, tx)


class Network:
    """
    A toy network/community that connects nodes and gossips transactions/blocks.

    This models the "community" portion of your definition:
    - agents (nodes) participate in validation
    - some broadcast transactions
    - gossip spreads data to peers

    Notes
    -----
    Real networks handle:
    - partial connectivity
    - adversarial peers
    - latency
    - duplicate suppression
    - bandwidth limits
    Here we keep it minimal for conceptual clarity.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}

    def add_node(self, node: Node) -> None:
        self._nodes[node.node_id] = node

    def broadcast_transaction(self, tx: Transaction, from_node_id: Optional[str] = None) -> None:
        """
        Send a transaction to all nodes (including the sender, if provided).

        Parameters
        ----------
        tx:
            The transaction to broadcast.
        from_node_id:
            Optional: who originated the broadcast (for logging/realism).
        """
        for node in self._nodes.values():
            node.receive_transaction(tx)

    def broadcast_block(self, block: Block, from_node_id: Optional[str] = None) -> None:
        """
        Send a block to all nodes.

        If any node rejects the block, it will raise ValueError. In real systems
        nodes reject locally without crashing the network.
        """
        for node in self._nodes.values():
            node.receive_block(block)


# ============================================================
# Example usage / simulation
# ============================================================

def example() -> None:
    """
    Demonstrate a small PoA blockchain network with 2 validators and a user transfer.
    """
    # Consensus config: authorized proposers and their secrets
    secrets = {"val1": "secret-1", "val2": "secret-2"}
    consensus = ProofOfAuthorityConsensus(proposer_secrets=secrets)

    # Transition rules
    transition = TokenTransferTransition()

    # Initial state (genesis)
    genesis = {
        "bal:alice": 100,
        "nonce:alice": 0,
        "bal:bob": 0,
        "nonce:bob": 0,
    }

    # Two full nodes
    n1 = Node("val1", state=KeyValueState(), transition=transition, consensus=consensus)
    n2 = Node("val2", state=KeyValueState(), transition=transition, consensus=consensus)

    n1.init_genesis(genesis)
    n2.init_genesis(genesis)

    net = Network()
    net.add_node(n1)
    net.add_node(n2)

    # Alice sends 25 tokens to Bob
    tx = Transaction(sender="alice", recipient="bob", amount=25, nonce=0)
    net.broadcast_transaction(tx, from_node_id="alice-client")

    # Validator 1 proposes and broadcasts a block including that tx
    block = n1.propose_block(proposer_secret=secrets["val1"])
    net.broadcast_block(block, from_node_id="val1")

    # Both nodes should converge on same state
    print("Node1 state:", n1.state.dump() if isinstance(n1.state, KeyValueState) else "unknown")
    print("Node2 state:", n2.state.dump() if isinstance(n2.state, KeyValueState) else "unknown")


if __name__ == "__main__":
    example()
