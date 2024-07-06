package io.collective.articles;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

import static java.util.Collections.emptyList;

public class ArticleDataGateway {
    private final List<ArticleRecord> articles = new ArrayList<>();
    private final Random sequence = new Random();

    public ArticleDataGateway() {
        this(emptyList());
    }

    public ArticleDataGateway(List<ArticleRecord> initialRecords) {
        articles.addAll(initialRecords);
    }

    public List<ArticleRecord> findAll() {
        return articles;
    }

    public List<ArticleRecord> findAvailable() {
        return articles.stream().filter(ArticleRecord::isAvailable).collect(Collectors.toList());
    }

    public void save(String title) {
        articles.add(new ArticleRecord(sequence.nextInt(), title, true));
    }

    public void clear() {
        articles.clear();
    }
}
