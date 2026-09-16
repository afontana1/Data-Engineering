FROM eclipse-temurin:21-alpine as jre-build

RUN $JAVA_HOME/bin/jlink \
 --add-modules java.base,java.desktop,java.sql,java.naming,java.management,java.net.http,jdk.jdwp.agent,jdk.crypto.ec \
 --strip-java-debug-attributes \
 --no-man-pages \
 --no-header-files \
 --compress=2 \
 --output /javaruntime

FROM alpine
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH "${JAVA_HOME}/bin:${PATH}"
COPY --from=jre-build /javaruntime $JAVA_HOME

RUN mkdir /opt/applications
COPY applications/provenance-server/build/libs/provenance-server-1.0-SNAPSHOT.jar /opt/applications/
CMD [ "java", "-jar", "/opt/applications/provenance-server-1.0-SNAPSHOT.jar" ]