package io.collective.endpoints;

public class EndpointRecord {
    private int id;
    private String name;

    public EndpointRecord(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }
}
