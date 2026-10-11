package test.collective.metrics;

import com.codahale.metrics.MetricRegistry;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.collective.metrics.HealthCheck;
import io.collective.metrics.MetricsController;
import io.collective.restsupport.BasicApp;
import io.collective.restsupport.RestTemplate;
import io.prometheus.client.CollectorRegistry;
import io.prometheus.client.dropwizard.DropwizardExports;
import org.eclipse.jetty.server.handler.HandlerList;
import org.jetbrains.annotations.NotNull;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class AppTest {
    BasicApp app;
    MetricRegistry registry;
    CollectorRegistry prometheus = CollectorRegistry.defaultRegistry;

    @Before
    public void setUp() {
        registry = new MetricRegistry();
        prometheus.register(new DropwizardExports(registry));

        app = new BasicApp(8888) {
            @NotNull
            @Override
            protected HandlerList handlerList() {
                HandlerList list = new HandlerList();
                list.addHandler(new HealthCheck());
                list.addHandler(new MetricsController(prometheus));
                list.addHandler(new TestController(new ObjectMapper(), registry));
                return list;
            }
        };
        app.start();
    }

    @After
    public void tearDown() {
        app.stop();
    }

    @Test
    public void metrics() {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/test-metrics", "application/json");
        assertEquals("test-requests=1", response);
    }

    @Test
    public void health() {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/health-check", "application/json");
        assertEquals("i'm healthy.", response);
    }

    @Test
    public void prometheus() {
        RestTemplate template = new RestTemplate();
        template.get("http://localhost:8888/test-metrics", "application/json");

        String response = template.get("http://localhost:8888/metrics", "text/plain; version=0.0.4; charset=utf-8");
        assertTrue(response.contains("test_requests_total 1.0"));
    }
}