# Blockchain Network

A *high-level* definition of blockchain, unifying “blockchain as database” + “blockchain as protocol” + “blockchain as social system.”

A blockchain network is:

1. **A replicated state** (or ledger) and an **append-only log** of state transitions (blocks/transactions) that deterministically define the latest state.

2. **A state transition function** (execution + validity rules) describing which transitions are allowed and how they update state.

3. **A consensus mechanism** (Sybil resistance, fork choice, finality rules) that selects a canonical ordering of blocks so all honest nodes converge on the same history/state.

4. **A participant set and incentive system** (users, builders, validators/nodes, clients) plus the **social layer** that coordinates upgrades and resolves ambiguity.

## Blockchain network in Python based on this definition:

* **Data structure (ledger/state):** `KeyValueState` (balances)
* **State transition rules (methods):** `TokenTransferTransition`
* **Consensus mechanism:** pluggable interface; implemented as **Proof-of-Authority** (PoA) for simplicity (`ProofOfAuthorityConsensus`)
* **Community/participants:** `Node` + `Network` that relays transactions/blocks

It’s written to follow **SOLID**:

* **S**RP: each class has one reason to change (state store vs mempool vs consensus vs networking).
* **O**CP: add a new consensus/transition/state store without changing `Node`.
* **L**SP: implementations conform to their interfaces.
* **I**SP: small interfaces (`ConsensusProtocol`, `StateTransitionFunction`, `StateStore`).
* **D**IP: `Node` depends on abstractions, injected via constructor.

1. Data structure: ledger/state + history

* **State:** `KeyValueState` stores balances/nonces.
* **History/order:** `ChainIndex` stores blocks, parents, heights; the canonical head is chosen by consensus.
* **“History of changes” nuance:** we store blocks; state is derived by replay (see `_rebuild_state_from_genesis_to_head`).

2. Methods / legal state changes

* `TokenTransferTransition` defines what a transaction *means* and when it is valid.
* The node uses it both for mempool admission and block execution.

3. Consensus protocol

* `ConsensusProtocol` is an interface.
* `ProofOfAuthorityConsensus` verifies proposer authorization + signature and chooses a head (longest chain).

4. Community / network participants

* `Network` simulates gossip.
* `Node` is a validating participant (full node).


## Important limitations 

* No fees, gas, signatures on transactions, peer-to-peer topology, or adversarial behavior.
* Rebuilding state is simplified and uses a `KeyValueState` convenience method; production clients need databases and snapshots.
* PoA is used for readability; you could swap in PoW/PoS by implementing `ConsensusProtocol` and injecting it.