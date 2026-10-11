package test.collective.rss;

import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import io.collective.rss.RSS;
import org.junit.Test;

import java.io.IOException;

import static org.junit.Assert.assertEquals;

public class RSSTest {

    @Test
    public void rss() throws IOException {
        String xml = new String(this.getClass().getResourceAsStream("/infoq.xml").readAllBytes());
        RSS rss = new XmlMapper().readValue(xml, RSS.class);
        assertEquals(15, rss.getChannel().getItem().size());
    }
}
