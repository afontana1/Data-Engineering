package test.collective.endpoints;

import com.codahale.metrics.MetricRegistry;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import io.collective.articles.ArticleDataGateway;
import io.collective.endpoints.EndpointTask;
import io.collective.endpoints.EndpointWorker;
import io.collective.restsupport.RestTemplate;
import io.collective.rss.Item;
import io.collective.rss.RSS;
import org.junit.Ignore;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class EndpointWorkerTest {
    private Logger logger = LoggerFactory.getLogger(this.getClass());

    @Test
    public void finder() throws IOException {
        String xml = new String(getClass().getResourceAsStream("/infoq.xml").readAllBytes());

        RestTemplate mock = mock(RestTemplate.class);
        when(mock.get("https://feed.infoq./", "application/xml")).thenReturn(xml);
        ArticleDataGateway gateway = new ArticleDataGateway(new MetricRegistry());

        EndpointWorker worker = new EndpointWorker(mock, gateway);
        worker.execute(new EndpointTask("https://feed.infoq./"));

        assertEquals(15, gateway.findAll().size());
    }

    @Ignore
    public void sequentialExample() throws IOException {
        int numberOfRequest = 80;
        for (int i = 0; i < numberOfRequest; i++) {
            RestTemplate template = new RestTemplate();
            EndpointTask task = new EndpointTask("https://feed.infoq./");
            String response = template.get(task.getEndpoint(), task.getAccept());
            RSS rss = new XmlMapper().readValue(response, RSS.class);
            logger.info("collected {} items from {}.", rss.getChannel().getItem().size(), task.getEndpoint());
        }
    }

    @Ignore
    public void concurrentExample() throws InterruptedException, ExecutionException {
        List<Callable<RSS>> callables = new ArrayList<>();

        int numberOfRequest = 80;
        for (int i = 0; i < numberOfRequest; i++) {

            callables.add(new Callable<RSS>() {
                @Override
                public RSS call() throws Exception {
                    RestTemplate template = new RestTemplate();
                    EndpointTask task = new EndpointTask("https://feed.infoq./");
                    String response = template.get(task.getEndpoint(), task.getAccept());
                    RSS rss = new XmlMapper().readValue(response, RSS.class);
                    logger.info("collected {} items from {}.", rss.getChannel().getItem().size(), task.getEndpoint());
                    return rss;
                }
            });
        }

        ExecutorService executorService = Executors.newFixedThreadPool(40);
        List<Future<RSS>> futures = executorService.invokeAll(callables);

        for (Future<RSS> future : futures) {
            RSS rss = future.get();
            List<Item> items = rss.getChannel().getItem();
            for (Item item : items) {
                String title = item.getTitle();
                if (title.contains("Google")) {
                    logger.info("found title=" + title);
                }
            }
        }
        executorService.shutdown();
    }
}