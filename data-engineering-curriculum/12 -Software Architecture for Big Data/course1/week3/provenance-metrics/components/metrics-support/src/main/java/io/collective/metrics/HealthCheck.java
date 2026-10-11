package io.collective.metrics;

import io.collective.restsupport.BasicHandler;
import org.eclipse.jetty.server.Request;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Arrays;

public class HealthCheck extends BasicHandler {
    @Override
    public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) {
        get("/health-check", Arrays.asList("application/json", "text/html"), baseRequest, response, () -> {
            try {
                response.setContentType("text/html; charset=UTF-8");
                response.getOutputStream().write("i'm healthy.".getBytes());
                response.setStatus(HttpServletResponse.SC_OK);
                baseRequest.setHandled(true);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }
}