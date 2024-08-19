package io.collective.workflow

import org.slf4j.LoggerFactory

open class NoopWorker(override val name: String = "noop-worker") : Worker<NoopTask> {
    private val logger = LoggerFactory.getLogger(this.javaClass)

    override fun execute(task: NoopTask) {
        logger.info("doing work. {} {}", task.name, task.value)
    }
}