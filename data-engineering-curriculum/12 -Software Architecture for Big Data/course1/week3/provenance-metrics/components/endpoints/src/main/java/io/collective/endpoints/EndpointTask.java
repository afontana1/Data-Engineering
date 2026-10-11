package io.collective.endpoints;

public class EndpointTask {
    private String endpoint;

    public EndpointTask(String endpoint) {
        this.endpoint = endpoint;
    }

    public String getEndpoint() {
        return endpoint;
    }

    public String getAccept() {
        return "application/xml";
    }
}