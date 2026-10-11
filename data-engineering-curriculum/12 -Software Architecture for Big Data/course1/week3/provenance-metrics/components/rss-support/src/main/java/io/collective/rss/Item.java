package io.collective.rss;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Item {
    @JacksonXmlProperty(isAttribute = true, localName = "title")
    private String title;

    public String getTitle() {
        return title;
    }

    @JacksonXmlProperty(isAttribute = true, namespace = "dc", localName = "creator")
    private String creator;

    public String getCreator() {
        return creator;
    }

    @JacksonXmlProperty(isAttribute = true, localName = "author")
    private String author;

    public String getAuthor() {
        return creator;
    }

}
