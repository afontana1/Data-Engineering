package test.collective.articles;

import com.codahale.metrics.MetricRegistry;
import io.collective.articles.ArticleDataGateway;
import io.collective.articles.ArticleRecord;
import org.junit.Before;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;

public class ArticleDataGatewayTest {
    @Before
    public void before() {

        ArticleDataGateway.articles = Arrays.asList(
                new ArticleRecord(10101, "Programming Languages InfoQ Trends Report - October 2019 4", true),
                new ArticleRecord(10102, "Single Page Applications and ASP.NET Core 3.0 2", false),
                new ArticleRecord(10103, "Google Open-Sources ALBERT Natural Language Model", true),
                new ArticleRecord(10104, "Ahead of re:Invent, Amazon Updates AWS Lambda", false),
                new ArticleRecord(10105, "Electron Desktop JavaScript Framework Finds a New Home", true),
                new ArticleRecord(10106, "Ryan Kitchens on Learning from Incidents at Netflix, the Role of SRE, and Sociotechnical Systems", true)
        );
    }

    @Test
    public void findAll() {
        ArticleDataGateway gateway = new ArticleDataGateway(new MetricRegistry());

        List<ArticleRecord> all = gateway.findAll();
        assertEquals(6, all.size());

        List<ArticleRecord> available = gateway.findAvailable();
        assertEquals(4, available.size());
    }
}
