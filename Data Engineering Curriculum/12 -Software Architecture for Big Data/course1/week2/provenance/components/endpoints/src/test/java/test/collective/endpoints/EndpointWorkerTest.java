package test.collective.endpoints;

import io.collective.articles.ArticleDataGateway;
import io.collective.endpoints.EndpointTask;
import io.collective.endpoints.EndpointWorker;
import io.collective.restsupport.RestTemplate;
import org.junit.Test;

import java.io.IOException;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class EndpointWorkerTest {
    @Test
    public void finder() throws IOException {
        String xml = new String(getClass().getResourceAsStream("/infoq.xml").readAllBytes());

        RestTemplate mock = mock(RestTemplate.class);
        when(mock.get("https://feed.infoq./", "application/xml")).thenReturn(xml);
        ArticleDataGateway gateway = new ArticleDataGateway();

        EndpointWorker worker = new EndpointWorker(mock, gateway);
        worker.execute(new EndpointTask("https://feed.infoq./"));

        assertEquals(15, gateway.findAll().size());
    }
}