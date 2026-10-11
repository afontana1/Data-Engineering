package io.collective.articles;

import com.codahale.metrics.Meter;
import com.codahale.metrics.MetricRegistry;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.collective.restsupport.BasicHandler;
import org.eclipse.jetty.server.Request;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ArticlesController extends BasicHandler {
    private ArticleDataGateway gateway;
    Meter articleRequests;
    Meter articleAvailableRequests;

    public ArticlesController(ObjectMapper mapper, ArticleDataGateway gateway, MetricRegistry registry) {
        super(mapper);
        this.gateway = gateway;
        this.articleRequests = registry.meter("article-requests");
        this.articleAvailableRequests = registry.meter("article-available-requests");
    }

    @Override
    public void handle(String target, Request request, HttpServletRequest servletRequest, HttpServletResponse servletResponse) {
        get("/articles", Arrays.asList("application/json", "text/html"), request, servletResponse, () -> {
            { // todo - query the articles gateway for *all* articles, map record to infos, and send back a collection of article infos
                ArrayList<ArticleInfo> articles = new ArrayList<>();
                List<ArticleRecord> all = gateway.findAll();
                for (ArticleRecord record : all) {
                    articles.add(new ArticleInfo(record.getId(), record.getTitle()));
                }
                writeJsonBody(servletResponse, articles);
            }
            articleRequests.mark();
        });

        get("/available", Arrays.asList("application/json", "text/html"), request, servletResponse, () -> {

            { // todo - query the articles gateway for *available* articles, map records to infos, and send back a collection of article infos
                ArrayList<ArticleInfo> articles = new ArrayList<>();
                List<ArticleRecord> all = gateway.findAvailable();
                for (ArticleRecord record : all) {
                    articles.add(new ArticleInfo(record.getId(), record.getTitle()));
                }
                writeJsonBody(servletResponse, articles);
            }
            articleAvailableRequests.mark();
        });
    }
}