package main.java.io.collective.provenance;

import java.util.ArrayList;
import java.util.List;

public class ProvenanceBlockchain {
    private List<ProvenanceBlock> chain;

    // Constructor to initialize the blockchain with the genesis block
    public ProvenanceBlockchain() {
        chain = new ArrayList<>();
        chain.add(createGenesisBlock());
    }

    // Create the genesis block
    private ProvenanceBlock createGenesisBlock() {
        return new ProvenanceBlock("0", "0", "Genesis Block", "system");
    }

    // Get the latest block
    public ProvenanceBlock getLatestBlock() {
        return chain.get(chain.size() - 1);
    }

    // Add a new block to the chain
    public void addBlock(String recordID, String updateDetails, String userID) {
        ProvenanceBlock latestBlock = getLatestBlock();
        ProvenanceBlock newBlock = new ProvenanceBlock(latestBlock.getHash(), recordID, updateDetails, userID);
        mineBlock(newBlock);
        chain.add(newBlock);
    }

    // Mine a block (proof of work)
    private void mineBlock(ProvenanceBlock block) {
        while (!block.getHash().startsWith("00")) {
            block.setNonce(block.getNonce() + 1);
            block.setHash(block.calculateHash());
        }
    }

    // Validate the blockchain
    public boolean isValid() {
        for (int i = 1; i < chain.size(); i++) {
            ProvenanceBlock currentBlock = chain.get(i);
            ProvenanceBlock previousBlock = chain.get(i - 1);

            if (!currentBlock.getHash().equals(currentBlock.calculateHash())) {
                return false;
            }

            if (!currentBlock.getPreviousHash().equals(previousBlock.getHash())) {
                return false;
            }
        }
        return true;
    }

    // Print the blockchain
    public void printBlockchain() {
        for (ProvenanceBlock block : chain) {
            System.out.println("Block:");
            System.out.println("  Previous Hash: " + block.getPreviousHash());
            System.out.println("  Record ID: " + block.getRecordID());
            System.out.println("  Update Details: " + block.getUpdateDetails());
            System.out.println("  User ID: " + block.getUserID());
            System.out.println("  Timestamp: " + block.getTimestamp());
            System.out.println("  Hash: " + block.getHash());
            System.out.println("  Nonce: " + block.getNonce());
            System.out.println();
        }
    }
}
