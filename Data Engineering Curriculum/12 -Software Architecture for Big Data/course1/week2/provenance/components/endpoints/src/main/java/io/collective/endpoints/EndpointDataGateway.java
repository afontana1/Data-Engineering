package io.collective.endpoints;

import java.util.Collections;
import java.util.List;

public class EndpointDataGateway {
    public List<EndpointRecord> findReady(String name) {
        if (!name.equals("ready")) {
            return Collections.emptyList();
        }

        return Collections.singletonList(
                new EndpointRecord(10101, "https://feed.infoq.com/") // always ready to collect data
        );
    }
}