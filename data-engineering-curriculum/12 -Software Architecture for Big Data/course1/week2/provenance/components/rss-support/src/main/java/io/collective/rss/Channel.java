package io.collective.rss;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlElementWrapper;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Channel {
    @JacksonXmlElementWrapper(useWrapping = false)
    private List<Item> item;

    public List<Item> getItem() {
        return item;
    }
}
