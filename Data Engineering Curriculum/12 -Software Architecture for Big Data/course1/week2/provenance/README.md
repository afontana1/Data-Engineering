# Provenance

A common architecture used for data collection.

Provenance collects and stores articles from [infoq.com](https://www.infoq.com/) and follows a
Netflix [Conductor-esque](https://netflix.github.io/conductor/) architecture.

### History

In 2016 we began a project to address some of the concerns around fake news. While most were analyzing articles, we
decided to take another approach; showing consumers where their content comes from. Our goal was to bring
source [journalist] context to the foreground.

### The exercise

Get the tests to pass!

- Query the articles gateway.
- Map rss results to a collection.
- Start the background worker.

Look for todo items in the codebase for where to get started.

### Quick start

Download the codebase.

Create a jar file without running tests.

```bash
./gradlew assemble
```

### Articles

Run the articles component tests to see what's failing.

```bash
./gradlew :components:articles:test
```

Review the *todo* comments in the `ArticlesController` class and get the tests to pass. Along the way it will be helpful
to use the `writeJsonBody` method to convert articles to json.

```java
writeJsonBody(servletResponse, articles);
```

### Endpoints

Run the endpoints component tests to see what's failing.

```bash
./gradlew :components:endpoints:test  
```

Review the *todo* comments in the EndpointWorker class and get the tests to pass. Along the way it will be helpful to
use `XmlMapper` to convert RSS feeds to Java objects.

```java
RSS rss = new XmlMapper().readValue(response, RSS.class);
```

### Test suite

Ensure all the tests pass.

```bash
./gradlew build
```

### Schedule work

Review *todo* comments in the `App` class within the provenance-server component. Create and start a `WorkScheduler`.

```java
WorkScheduler<EndpointTask> scheduler = new WorkScheduler<>(finder, workers, 300);
``` 

_Pro tip:_ review the `testScheduler` test in the `WorkSchedulerTest` class.

### Run locally

Build the application again then run it locally to ensure that the endpoint worker is collecting articles.

```bash
./gradlew build
java -jar applications/provenance-server/build/libs/provenance-server-1.0-SNAPSHOT.jar 
```

Make a request for all articles in another terminal window.

```bash
curl -H "Accept: application/json" http://localhost:8881/articles
```

## Run with Docker

1. Build with Docker.
   ```bash
    docker build -t provenance-server . --platform linux/amd64
    ```

1. Run with Docker.
   ```bash
   docker run -p 8881:8881 provenance-server
   ```

Hope you enjoy the exercise!

Thanks,

The IC Team

© 2022 by Initial Capacity, Inc. All rights reserved.