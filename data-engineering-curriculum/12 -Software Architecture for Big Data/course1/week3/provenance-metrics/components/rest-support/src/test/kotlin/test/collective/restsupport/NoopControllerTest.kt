package test.collective.restsupport

import io.collective.restsupport.BasicApp
import io.collective.restsupport.NoopController
import io.collective.restsupport.RestTemplate
import org.eclipse.jetty.server.handler.HandlerList
import org.junit.After
import org.junit.Before
import org.junit.Test
import kotlin.test.assertEquals

class NoopControllerTest {
    val template = RestTemplate()

    private var app: BasicApp = object : BasicApp(8888) {
        override fun handlerList() = HandlerList().apply {
            addHandler(NoopController())
        }
    }

    @Before
    fun setUp() {
        app.start()
    }

    @After
    fun tearDown() {
        app.stop()
    }

    @Test
    fun testGet() {
        val response = template.get("http://localhost:8888/", "*/*")
        assertEquals("Noop!", response)
    }
}