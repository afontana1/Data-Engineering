package io.collective.workflow

interface Worker<T> {
    val name: String

    @Throws(Exception::class)
    fun execute(task: T)
}