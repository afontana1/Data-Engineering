```plantuml
@startuml
!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(user, "End User", "Uploads docs via browser UI")
Person(producer, "Offline Producer", "Batch submits jobs")

System_Boundary(sys, "Document Parsing Platform") {
  Container(api, "Job API", "API Gateway + Lambda OR ECS(FastAPI)", "Creates jobs, presigns uploads, starts workflows, serves polling")
  Container(workflow, "Orchestrator", "AWS Step Functions (Standard)", "Controls split->extract->postprocess; retries/timeouts")
  Container(splitter, "PDF Splitter", "ECS/Fargate Task", "Splits oversized PDFs into parts (<= 500MB each)")
  Container(post, "Post-Processor", "ECS/Fargate Task", "Merges Textract results; produces canonical JSON/Markdown")
  ContainerDb(ddb, "Job Store", "DynamoDB", "Job state for polling")
  ContainerDb(rawS3, "Raw Storage", "S3 Bucket", "Input PDFs + split parts")
  ContainerDb(parsedS3, "Parsed Storage", "S3 Bucket", "Textract raw outputs + final canonical outputs")
}

System_Ext(textract, "Amazon Textract", "Async document analysis (tables/forms/text)")
System_Ext(cw, "CloudWatch", "Logs/metrics/alarms")

Rel(user, api, "Create job / start / poll / fetch", "HTTPS")
Rel(producer, api, "Create job / start / poll / fetch", "HTTPS")

Rel(api, rawS3, "Presign uploads / validate objects")
Rel(api, ddb, "Create/update/read job state")
Rel(api, workflow, "StartExecution(jobId)")

Rel(workflow, splitter, "RunTask(jobId, input)")
Rel(splitter, rawS3, "Read original; write parts")

Rel(workflow, textract, "StartDocumentAnalysis + poll GetDocumentAnalysis")
Rel(workflow, parsedS3, "Optionally store raw Textract pages/chunks")

Rel(workflow, post, "RunTask(jobId, parts, textract refs)")
Rel(post, parsedS3, "Write document.json (+.md)")
Rel(post, ddb, "Set SUCCEEDED/FAILED + output pointer")

Rel(api, parsedS3, "Presign result download")

Rel(api, cw, "Logs/metrics")
Rel(workflow, cw, "Logs/metrics")
Rel(splitter, cw, "Logs/metrics")
Rel(post, cw, "Logs/metrics")

SHOW_LEGEND()
@enduml
```