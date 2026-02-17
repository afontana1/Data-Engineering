```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(user, "End User", "Uploads documents and retrieves parsed results via UI")
Person(producer, "Offline Producer", "Batch submits jobs programmatically")
Person(ops, "Ops/Admin", "Monitors system health, failures, and costs")

System_Boundary(sys, "Document Parsing Platform") {
  System(system, "Document Parsing Platform", "Async document parsing + normalization into canonical JSON output")
}

System_Ext(textract, "Amazon Textract", "Async OCR + tables/forms extraction")
System_Ext(s3, "Amazon S3", "Raw and parsed object storage")
System_Ext(ddb, "Amazon DynamoDB", "Job state store for polling")
System_Ext(cw, "Amazon CloudWatch", "Logs, metrics, alarms")

Rel(user, system, "Create job / upload / start / poll / fetch result", "HTTPS")
Rel(producer, system, "Create job / upload / start / poll / fetch result", "HTTPS")
Rel(ops, system, "Observe and operate", "AWS Console / dashboards")

Rel(system, s3, "Stores raw + parsed artifacts")
Rel(system, ddb, "Reads/writes job states")
Rel(system, textract, "Starts and polls async analysis")
Rel(system, cw, "Emits logs/metrics")

SHOW_LEGEND()
@enduml
```