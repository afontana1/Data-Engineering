package io.collective

import java.time.Clock
import java.time.Instant

class SimpleAgedKache {
    private val clock: Clock
    private var head: Node? = null
    private var size = 0

    constructor(clock: Clock?) {
        this.clock = clock ?: Clock.systemDefaultZone()
    }

    constructor() {
        this.clock = Clock.systemDefaultZone()
    }

    fun put(key: Any?, value: Any?, retentionInMillis: Int) {
        val expiryTime = clock.instant().plusMillis(retentionInMillis.toLong())
        val newNode = Node(key, value, expiryTime)
        
        if (head == null) {
            head = newNode
        } else {
            var current = head
            while (current!!.next != null) {
                current = current.next
            }
            current.next = newNode
        }
        size++
    }

    fun isEmpty(): Boolean {
        cleanUp()
        return size == 0
    }

    fun size(): Int {
        cleanUp()
        return size
    }

    fun get(key: Any?): Any? {
        cleanUp()
        var current = head
        while (current != null) {
            if (current.key == key && !current.isExpired(clock.instant())) {
                return current.value
            }
            current = current.next
        }
        return null
    }

    private fun cleanUp() {
        val now = clock.instant()
        while (head != null && head!!.isExpired(now)) {
            head = head!!.next
            size--
        }
        var current = head
        while (current != null && current.next != null) {
            if (current.next!!.isExpired(now)) {
                current.next = current.next!!.next
                size--
            } else {
                current = current.next
            }
        }
    }

    private class Node(val key: Any?, val value: Any?, val expiryTime: Instant) {
        var next: Node? = null

        fun isExpired(now: Instant): Boolean {
            return now.isAfter(expiryTime)
        }
    }
}
