package test.collective.start;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.collective.articles.ArticleInfo;
import io.collective.restsupport.RestTemplate;
import io.collective.start.App;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class AppTest {
    App app;

    @Before
    public void setUp() throws Exception {
        app = new App(8888);
        app.start();
    }

    @After
    public void tearDown() {
        app.stop();
    }

    @Test
    public void slash() {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/", "application/json");
        assertEquals("Noop!", response);
    }

    @Test
    public void health() {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/health-check", "application/json");
        assertEquals("i'm healthy.", response);
    }

    @Test
    public void metrics() {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/metrics", "text/plain; version=0.0.4; charset=utf-8");
        assertTrue(response.contains("articles"));
        assertTrue(response.contains("article_requests_total"));
        assertTrue(response.contains("article_available_requests_total"));
    }

    @Test
    public void articles() throws Exception {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/articles", "application/json");

        List<ArticleInfo> entries = new ObjectMapper().readValue(response, new TypeReference<List<ArticleInfo>>() {
        });
        assertTrue(true);
    }
}