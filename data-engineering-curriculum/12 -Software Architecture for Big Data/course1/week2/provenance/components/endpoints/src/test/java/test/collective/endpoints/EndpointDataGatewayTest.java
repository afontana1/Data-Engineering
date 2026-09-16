package test.collective.endpoints;

import io.collective.endpoints.EndpointDataGateway;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class EndpointDataGatewayTest {

    @Test
    public void readdy() {
        EndpointDataGateway gateway = new EndpointDataGateway();

        assertEquals(1, gateway.findReady("ready").size());
        assertEquals(0, gateway.findReady("not-ready").size());
    }
}