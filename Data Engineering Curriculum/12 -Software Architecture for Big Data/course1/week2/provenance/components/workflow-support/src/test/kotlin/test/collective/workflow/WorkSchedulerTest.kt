package test.collective.workflow

import com.nhaarman.mockito_kotlin.any
import com.nhaarman.mockito_kotlin.spy
import com.nhaarman.mockito_kotlin.times
import com.nhaarman.mockito_kotlin.verify
import io.collective.workflow.NoopTask
import io.collective.workflow.NoopWorkFinder
import io.collective.workflow.NoopWorker
import io.collective.workflow.WorkScheduler
import org.junit.Test
import java.util.*

class WorkSchedulerTest {
    @Test
    fun testScheduler() {
        val finder = NoopWorkFinder();
        val worker = NoopWorker()
        val spy = spy(worker);
        val scheduler = WorkScheduler<NoopTask>(finder, Collections.singletonList(spy))

        scheduler.start();

        verify(spy, times(1)).execute(any())

        scheduler.shutdown()
    }
}