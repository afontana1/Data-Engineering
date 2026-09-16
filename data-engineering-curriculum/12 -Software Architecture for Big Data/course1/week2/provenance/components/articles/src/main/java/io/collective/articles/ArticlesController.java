package io.collective.articles;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.collective.restsupport.BasicHandler;
import org.eclipse.jetty.server.Request;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.List;
import java.util.stream.Collectors;

public class ArticlesController extends BasicHandler {
    private final ArticleDataGateway gateway;

    public ArticlesController(ObjectMapper mapper, ArticleDataGateway gateway) {
        super(mapper);
        this.gateway = gateway;
    }

    @Override
    public void handle(String target, Request request, HttpServletRequest servletRequest, HttpServletResponse servletResponse) {
        get("/articles", List.of("application/json", "text/html"), request, servletResponse, () -> {
            // Query the articles gateway for *all* articles
            List<ArticleRecord> records = gateway.findAll();
            // Map records to infos
            List<ArticleInfo> infos = records.stream()
                    .map(record -> new ArticleInfo(record.getId(), record.getTitle()))
                    .collect(Collectors.toList());
            // Send back a collection of article infos
            writeJsonBody(servletResponse, infos);
        });

        get("/available", List.of("application/json"), request, servletResponse, () -> {
            // Query the articles gateway for *available* articles
            List<ArticleRecord> records = gateway.findAvailable();
            // Map records to infos
            List<ArticleInfo> infos = records.stream()
                    .map(record -> new ArticleInfo(record.getId(), record.getTitle()))
                    .collect(Collectors.toList());
            // Send back a collection of article infos
            writeJsonBody(servletResponse, infos);
        });
    }
}
