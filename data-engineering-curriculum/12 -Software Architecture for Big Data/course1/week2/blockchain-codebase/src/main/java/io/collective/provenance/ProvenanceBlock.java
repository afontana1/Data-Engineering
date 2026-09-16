package main.java.io.collective.provenance;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class ProvenanceBlock {
    private String previousHash;
    private String recordID;
    private String updateDetails;
    private String userID;
    private long timestamp;
    private String hash;
    private int nonce;

    // Constructor
    public ProvenanceBlock(String previousHash, String recordID, String updateDetails, String userID) {
        this.previousHash = previousHash;
        this.recordID = recordID;
        this.updateDetails = updateDetails;
        this.userID = userID;
        this.timestamp = System.currentTimeMillis();
        this.nonce = 0;
        this.hash = calculateHash();
    }

    // Calculate the hash of the block
    public String calculateHash() {
        return SHA256(previousHash + recordID + updateDetails + userID + timestamp + nonce);
    }

    // Simple SHA-256 hashing function
    private String SHA256(String input) {
        MessageDigest digest;
        try {
            digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
            return String.format("%064x", new BigInteger(1, hash));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    // Getters
    public String getPreviousHash() {
        return previousHash;
    }

    public String getRecordID() {
        return recordID;
    }

    public String getUpdateDetails() {
        return updateDetails;
    }

    public String getUserID() {
        return userID;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public String getHash() {
        return hash;
    }

    public int getNonce() {
        return nonce;
    }
}
