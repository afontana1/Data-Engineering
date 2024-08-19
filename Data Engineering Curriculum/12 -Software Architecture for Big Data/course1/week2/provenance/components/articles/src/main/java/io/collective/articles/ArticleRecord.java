package io.collective.articles;

public class ArticleRecord {
    private int id;
    private String title;
    private boolean available;

    public ArticleRecord(int id, String title, boolean available) {
        this.id = id;
        this.title = title;
        this.available = available;
    }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public boolean isAvailable() {
        return available;
    }
}
