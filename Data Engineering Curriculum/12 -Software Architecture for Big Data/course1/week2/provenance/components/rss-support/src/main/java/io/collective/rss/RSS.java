package io.collective.rss;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlProperty;
import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlRootElement;

@JacksonXmlRootElement(localName = "rss")
@JsonIgnoreProperties(ignoreUnknown = true)
public class RSS {
    @JacksonXmlProperty(isAttribute = true)
    private Channel channel;

    public Channel getChannel() {
        return channel;
    }
}
