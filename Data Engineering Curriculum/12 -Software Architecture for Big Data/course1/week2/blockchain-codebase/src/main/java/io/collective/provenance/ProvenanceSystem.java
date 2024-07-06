package main.java.io.collective.provenance;

public class ProvenanceSystem {
    private ProvenanceBlockchain blockchain;

    public ProvenanceSystem() {
        blockchain = new ProvenanceBlockchain();
    }

    // Update record in the database and record the change in the blockchain
    public void updateRecord(String recordID, String updateDetails, String userID) {
        // Update the database (pseudo-code)
        // Database.update(recordID, updateDetails);

        // Record the update in the blockchain
        blockchain.addBlock(recordID, updateDetails, userID);
    }

    // Verify the blockchain integrity
    public boolean verifyProvenance() {
        return blockchain.isValid();
    }

    // Main method for demonstration
    public static void main(String[] args) {
        ProvenanceSystem provenanceSystem = new ProvenanceSystem();

        // Simulate updates
        provenanceSystem.updateRecord("product123", "Updated price to $100", "user1");
        provenanceSystem.updateRecord("product123", "Updated description", "user2");

        // Verify and print the blockchain
        if (provenanceSystem.verifyProvenance()) {
            System.out.println("Blockchain is valid.");
        } else {
            System.out.println("Blockchain is not valid.");
        }

        // Print the blockchain
        provenanceSystem.blockchain.printBlockchain();
    }
}
