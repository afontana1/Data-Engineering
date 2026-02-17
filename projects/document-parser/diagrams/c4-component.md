```plantuml
@startuml
!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

Container_Boundary(apiBoundary, "Job API (Lambda or FastAPI service)") {
  Component(auth, "AuthN/AuthZ", "Middleware", "Validates caller identity, tenant context")
  Component(jobCtrl, "Jobs Controller", "HTTP handlers", "POST /jobs, POST /start, GET /jobs/{id}, GET /result")
  Component(presign, "Presign Service", "S3 SDK", "Generates presigned PUT/GET URLs")
  Component(jobRepo, "Job Repository", "DynamoDB SDK", "CRUD job records and status")
  Component(execStarter, "Execution Starter", "SFN SDK", "Starts Step Functions executions")
}

Container_Boundary(wfBoundary, "Orchestrator (Step Functions)") {
  Component(wfInit, "Init/Validate", "State(s)", "Validate S3 input; set STARTED")
  Component(wfSplit, "Split Stage", "ECS RunTask", "Split if >500MB/policy")
  Component(wfMap, "Extract Map", "Map State", "Process each part with Textract async + pagination")
  Component(wfPost, "Post-Process Stage", "ECS RunTask", "Merge/normalize; output canonical schema")
  Component(wfFinalize, "Finalize", "State(s)", "Set SUCCEEDED/FAILED and store pointers")
}

System_Ext(s3, "S3 (Raw/Parsed)", "Object storage")
System_Ext(ddb, "DynamoDB", "Job store")
System_Ext(textract, "Textract", "Async extraction")
System_Ext(cw, "CloudWatch", "Logs/metrics")

Rel(jobCtrl, auth, "invokes")
Rel(jobCtrl, presign, "requests presigned URLs")
Rel(jobCtrl, jobRepo, "reads/writes job state")
Rel(jobCtrl, execStarter, "starts workflow")
Rel(presign, s3, "uses")
Rel(jobRepo, ddb, "uses")
Rel(execStarter, wfInit, "starts execution")

Rel(wfInit, s3, "HeadObject/validate")
Rel(wfInit, jobRepo, "update STARTED")
Rel(wfSplit, s3, "read/write parts")
Rel(wfMap, textract, "start/poll/get pages")
Rel(wfMap, s3, "write raw results (optional)")
Rel(wfPost, s3, "read raw results; write canonical outputs")
Rel(wfFinalize, jobRepo, "update SUCCEEDED/FAILED")
Rel(apiBoundary, cw, "logs/metrics")
Rel(wfBoundary, cw, "logs/metrics")

SHOW_LEGEND()
@enduml
```