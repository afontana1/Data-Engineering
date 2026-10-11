package io.collective.metrics;

import io.collective.restsupport.BasicHandler;
import io.prometheus.client.CollectorRegistry;
import io.prometheus.client.exporter.common.TextFormat;
import org.eclipse.jetty.server.Request;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;

public class MetricsController extends BasicHandler {
    private CollectorRegistry registry;

    public MetricsController(CollectorRegistry registry) {
        this.registry = registry;
    }

    @Override
    public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) {
        get("/metrics", Arrays.asList("application/json", "text/html", "text/plain"), baseRequest, response, () -> {
            try {
                response.setContentType("text/plain");
                writeMetrics(response);
                response.setStatus(HttpServletResponse.SC_OK);
                baseRequest.setHandled(true);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }

    private void writeMetrics(HttpServletResponse response) throws IOException {
        PrintWriter writer = response.getWriter();
        TextFormat.write004(writer, registry.metricFamilySamples());
        writer.flush();
    }
}