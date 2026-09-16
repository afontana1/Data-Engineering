package test.collective.endpoints;

import io.collective.endpoints.EndpointDataGateway;
import io.collective.endpoints.EndpointTask;
import io.collective.endpoints.EndpointWorkFinder;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.assertEquals;

public class EndpointWorkFinderTest {
    @Test
    public void finder() {
        EndpointWorkFinder finder = new EndpointWorkFinder(new EndpointDataGateway());

        List<EndpointTask> ready = finder.findRequested("ready");
        assertEquals(1, ready.size());

        List<EndpointTask> other = finder.findRequested("not-ready");
        assertEquals(0, other.size());
    }
}
