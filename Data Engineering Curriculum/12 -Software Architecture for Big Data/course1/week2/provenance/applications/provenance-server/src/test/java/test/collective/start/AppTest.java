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

public class AppTest {
    App app;

    @Before
    public void setUp() throws Exception {
        app = new App(8888);
        app.start();
    }

    @After
    public void tearDown() throws Exception {
        app.stop();
    }

    @Test
    public void slash() throws Exception {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/", "application/json");
        assertEquals("Noop!", response);
    }

    @Test
    public void articles() throws Exception {
        RestTemplate template = new RestTemplate();
        String response = template.get("http://localhost:8888/articles", "application/json");

        List<ArticleInfo> entries = new ObjectMapper().readValue(response, new TypeReference<List<ArticleInfo>>() {
        });
        assertEquals(2, entries.size());
    }
}
