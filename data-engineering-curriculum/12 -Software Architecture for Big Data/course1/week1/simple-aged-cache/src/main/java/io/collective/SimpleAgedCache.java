package io.collective;

import java.time.Clock;
import java.time.Instant;

public class SimpleAgedCache {

    private final Clock clock;
    private Node head;
    private int size;

    public SimpleAgedCache(Clock clock) {
        this.clock = clock;
        this.head = null;
        this.size = 0;
    }

    public SimpleAgedCache() {
        this(Clock.systemDefaultZone());
    }

    public void put(Object key, Object value, int retentionInMillis) {
        Instant expiryTime = clock.instant().plusMillis(retentionInMillis);
        Node newNode = new Node(key, value, expiryTime);
        
        if (head == null) {
            head = newNode;
        } else {
            Node current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }

    public boolean isEmpty() {
        cleanUp();
        return size == 0;
    }

    public int size() {
        cleanUp();
        return size;
    }

    public Object get(Object key) {
        cleanUp();
        Node current = head;
        while (current != null) {
            if (current.key.equals(key) && !current.isExpired(clock.instant())) {
                return current.value;
            }
            current = current.next;
        }
        return null;
    }

    private void cleanUp() {
        Instant now = clock.instant();
        while (head != null && head.isExpired(now)) {
            head = head.next;
            size--;
        }
        Node current = head;
        while (current != null && current.next != null) {
            if (current.next.isExpired(now)) {
                current.next = current.next.next;
                size--;
            } else {
                current = current.next;
            }
        }
    }

    private static class Node {
        Object key;
        Object value;
        Instant expiryTime;
        Node next;

        Node(Object key, Object value, Instant expiryTime) {
            this.key = key;
            this.value = value;
            this.expiryTime = expiryTime;
            this.next = null;
        }

        boolean isExpired(Instant now) {
            return now.isAfter(expiryTime);
        }
    }
}


// Implementation with built in data structures
// package io.collective;

// import java.time.Clock;
// import java.time.Instant;
// import java.util.HashMap;
// import java.util.Map;

// public class SimpleAgedCache {

//     private final Clock clock;
//     private final Map<Object, CacheEntry> cache;

//     public SimpleAgedCache(Clock clock) {
//         this.clock = clock;
//         this.cache = new HashMap<>();
//     }

//     public SimpleAgedCache() {
//         this(Clock.systemDefaultZone());
//     }

//     public void put(Object key, Object value, int retentionInMillis) {
//         Instant expiryTime = clock.instant().plusMillis(retentionInMillis);
//         cache.put(key, new CacheEntry(value, expiryTime));
//     }

//     public boolean isEmpty() {
//         cleanUp();
//         return cache.isEmpty();
//     }

//     public int size() {
//         cleanUp();
//         return cache.size();
//     }

//     public Object get(Object key) {
//         cleanUp();
//         CacheEntry entry = cache.get(key);
//         return (entry == null || entry.isExpired(clock.instant())) ? null : entry.getValue();
//     }

//     private void cleanUp() {
//         Instant now = clock.instant();
//         cache.entrySet().removeIf(entry -> entry.getValue().isExpired(now));
//     }

//     private static class CacheEntry {
//         private final Object value;
//         private final Instant expiryTime;

//         CacheEntry(Object value, Instant expiryTime) {
//             this.value = value;
//             this.expiryTime = expiryTime;
//         }

//         Object getValue() {
//             return value;
//         }

//         boolean isExpired(Instant now) {
//             return now.isAfter(expiryTime);
//         }
//     }
// }
