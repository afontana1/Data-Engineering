package io.collective.restsupport

import com.fasterxml.jackson.databind.ObjectMapper
import org.eclipse.jetty.http.HttpMethod
import org.eclipse.jetty.server.Request
import org.eclipse.jetty.server.handler.AbstractHandler
import java.io.IOException
import javax.servlet.http.HttpServletResponse

abstract class BasicHandler(private val mapper: ObjectMapper = ObjectMapper()) : AbstractHandler() {

    fun post(uri: String, supportedMediaTypes: List<String>, request: Request, httpServletResponse: HttpServletResponse, block: Runnable) {
        if (request.method == HttpMethod.POST.toString()) {
            if (uri == request.requestURI) {
                val acceptedMediaType = request.getHeader("Accept")

                for (supportedMediaType in supportedMediaTypes) {
                    if (acceptedMediaType.contains(supportedMediaType)) {
                        httpServletResponse.contentType = supportedMediaType
                        try {
                            httpServletResponse.status = HttpServletResponse.SC_CREATED
                            block.run()
                        } catch (e: IOException) {
                            httpServletResponse.status = HttpServletResponse.SC_INTERNAL_SERVER_ERROR
                        }
                        request.isHandled = true
                    }
                }
            }
        }
    }

    fun get(uri: String, supportedMediaTypes: List<String>, request: Request, httpServletResponse: HttpServletResponse, block: Runnable) {
        if (request.method == HttpMethod.GET.toString()) {
            if (uri == request.requestURI) {
                val acceptedMediaType = request.getHeader("Accept")

                for (supportedMediaType in supportedMediaTypes) {
                    if (acceptedMediaType.contains(supportedMediaType)) {
                        httpServletResponse.contentType = supportedMediaType
                        try {
                            block.run()
                            httpServletResponse.status = HttpServletResponse.SC_OK
                        } catch (e: IOException) {
                            httpServletResponse.status = HttpServletResponse.SC_INTERNAL_SERVER_ERROR
                        }
                        request.isHandled = true
                    }
                }
            }
        }
    }

    protected fun writeJsonBody(servletResponse: HttpServletResponse, subject: Any?) {
        mapper.writeValue(servletResponse.outputStream, subject);
    }
}