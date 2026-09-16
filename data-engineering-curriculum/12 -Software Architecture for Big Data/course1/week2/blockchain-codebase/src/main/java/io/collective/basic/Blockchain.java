package io.collective.basic;

import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;

public class Blockchain {
    private final List<Block> chain;

    public Blockchain() {
        this.chain = new ArrayList<>();
    }

    public boolean isEmpty() {
        return chain.isEmpty();
    }

    public void add(Block block) {
        chain.add(block);
    }

    public int size() {
        return chain.size();
    }

    public boolean isValid() throws NoSuchAlgorithmException {
        if (chain.isEmpty()) {
            return true; // An empty chain is considered valid
        }

        for (int i = 1; i < chain.size(); i++) {
            Block currentBlock = chain.get(i);
            Block previousBlock = chain.get(i - 1);

            // Check if the current block is mined
            if (!Blockchain.isMined(currentBlock)) {
                return false;
            }

            // Check if the previous hash matches
            if (!currentBlock.getPreviousHash().equals(previousBlock.getHash())) {
                return false;
            }

            // Check if the hash is correctly calculated
            if (!currentBlock.getHash().equals(currentBlock.calculatedHash())) {
                return false;
            }
        }

        // Special check for the first block in the chain (genesis block)
        Block genesisBlock = chain.get(0);
        if (!Blockchain.isMined(genesisBlock) || !genesisBlock.getHash().equals(genesisBlock.calculatedHash())) {
            return false;
        }

        return true;
    }

    public static Block mine(Block block) throws NoSuchAlgorithmException {
        int nonce = 0;
        Block mined;
        do {
            mined = new Block(block.getPreviousHash(), block.getTimestamp(), nonce);
            nonce++;
        } while (!isMined(mined));
        return mined;
    }

    public static boolean isMined(Block minedBlock) {
        return minedBlock.getHash().startsWith("00");
    }
}
