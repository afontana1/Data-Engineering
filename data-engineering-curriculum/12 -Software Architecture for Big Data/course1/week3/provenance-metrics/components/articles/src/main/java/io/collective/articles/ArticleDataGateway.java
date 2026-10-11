package io.collective.articles;

import com.codahale.metrics.CachedGauge;
import com.codahale.metrics.MetricRegistry;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

public class ArticleDataGateway {
    public static List<ArticleRecord> articles = new ArrayList<>();

    private Random sequence = new Random();

    public ArticleDataGateway(MetricRegistry registry) {
        registry.register("articles",
                new CachedGauge<Integer>(10, TimeUnit.MINUTES) {
                    @Override
                    protected Integer loadValue() {
                        return articles.size();
                    }
                });
    }

    public List<ArticleRecord> findAll() {
        return articles;
    }

    public List<ArticleRecord> findAvailable() {
        return articles.stream().filter(ArticleRecord::isAvailable).collect(Collectors.toList());
    }

    public void save(ArticleInfo info) {
        articles.add(new ArticleRecord(sequence.nextInt(), info.getTitle(), true));
    }
}