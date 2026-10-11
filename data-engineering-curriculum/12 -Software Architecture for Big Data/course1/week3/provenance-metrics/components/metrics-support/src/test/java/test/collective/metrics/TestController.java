package test.collective.metrics;

import com.codahale.metrics.Meter;
import com.codahale.metrics.MetricRegistry;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.collective.restsupport.BasicHandler;
import org.eclipse.jetty.server.Request;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Arrays;

public class TestController extends BasicHandler {
    private final Meter meter;

    public TestController(ObjectMapper mapper, MetricRegistry registry) {
        super(mapper);
        this.meter = registry.meter("test-requests");
    }

    @Override
    public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) {
        get("/test-metrics", Arrays.asList("application/json", "text/html"), baseRequest, response, () -> {
            meter.mark();
            try {
                response.setContentType("text/html; charset=UTF-8");
                response.getOutputStream().write(("test-requests=" + meter.getCount()).getBytes());
                response.setStatus(HttpServletResponse.SC_OK);
                baseRequest.setHandled(true);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }
}