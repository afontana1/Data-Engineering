package io.collective.start;

import com.codahale.metrics.MetricRegistry;
import com.codahale.metrics.Slf4jReporter;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.collective.articles.ArticleDataGateway;
import io.collective.articles.ArticleRecord;
import io.collective.articles.ArticlesController;
import io.collective.endpoints.EndpointDataGateway;
import io.collective.endpoints.EndpointTask;
import io.collective.endpoints.EndpointWorkFinder;
import io.collective.endpoints.EndpointWorker;
import io.collective.metrics.HealthCheck;
import io.collective.metrics.MetricsController;
import io.collective.restsupport.BasicApp;
import io.collective.restsupport.NoopController;
import io.collective.restsupport.RestTemplate;
import io.collective.workflow.WorkScheduler;
import io.collective.workflow.Worker;
import io.prometheus.client.CollectorRegistry;
import io.prometheus.client.dropwizard.DropwizardExports;
import org.eclipse.jetty.server.handler.HandlerList;
import org.jetbrains.annotations.NotNull;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.TimeZone;
import java.util.concurrent.TimeUnit;


public class App extends BasicApp {
    MetricRegistry registry = new MetricRegistry();
    ArticleDataGateway gateway = new ArticleDataGateway(registry);
    CollectorRegistry prometheus = CollectorRegistry.defaultRegistry;

    Slf4jReporter reporter = Slf4jReporter.forRegistry(registry)
            .outputTo(LoggerFactory.getLogger("io.collective.start"))
            .convertRatesTo(TimeUnit.SECONDS)
            .convertDurationsTo(TimeUnit.MILLISECONDS)
            .build();

    @Override
    public void start() {
        prometheus.register(new DropwizardExports(registry));
        reporter.start(5, TimeUnit.SECONDS);
        super.start();

        ArticleDataGateway.articles = new ArrayList<>();
        ArticleDataGateway.articles.add(new ArticleRecord(10101, "Programming Languages InfoQ Trends Report - October 2019 4", true));
        ArticleDataGateway.articles.add(new ArticleRecord(10106, "Ryan Kitchens on Learning from Incidents at Netflix, the Role of SRE, and Sociotechnical Systems", true));

        { // todo - start the endpoint worker
            EndpointWorkFinder finder = new EndpointWorkFinder(new EndpointDataGateway());
            EndpointWorker worker = new EndpointWorker(new RestTemplate(), gateway);
            List<Worker<EndpointTask>> workers = Collections.singletonList(worker);
            WorkScheduler<EndpointTask> scheduler = new WorkScheduler<>(finder, workers, 300);
            scheduler.start();
        }
    }

    public App(int port) {
        super(port);
    }

    @NotNull
    @Override
    protected HandlerList handlerList() {
        HandlerList list = new HandlerList();
        list.addHandler(new ArticlesController(new ObjectMapper(), gateway, registry));
        list.addHandler(new HealthCheck());
        list.addHandler(new MetricsController(prometheus));
        list.addHandler(new NoopController());
        return list;
    }

    public static void main(String[] args) {
        TimeZone.setDefault(TimeZone.getTimeZone("UTC"));
        String port = System.getenv("PORT") != null ? System.getenv("PORT") : "8881";
        App app = new App(Integer.parseInt(port));
        app.start();
    }
}