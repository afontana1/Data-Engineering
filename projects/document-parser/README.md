# Document Parser Platform (AWS) — Deployment README (Windows CMD)

This repo deploys an **async document parsing pipeline** on AWS using:

- **API Gateway + Lambda** for job submission and polling
- **S3** for raw uploads and parsed outputs
- **DynamoDB** for job state + progress
- **Step Functions** as the orchestrator
- **ECS Fargate** tasks for `splitter` and `postprocess`
- **Amazon Textract** for text/table extraction (no GPUs required)
- **ECR** for container images

> This README documents **exactly what we did** to deploy from a Windows machine using **CMD**, Docker Desktop, and AWS CLI.

---

## Project structure

```

document-parser/
splitter/
Dockerfile
splitter.py
requirements.txt
postprocess/
Dockerfile
postprocess.py
requirements.txt
doc-parsing-platform.yml

## Prerequisites

### 1) Install Docker Desktop
- Install Docker Desktop for Windows
- Ensure it’s running (you can run `docker version` in CMD)

### 2) Install AWS CLI v2 (Windows)
Download and run the official MSI:
- https://awscli.amazonaws.com/AWSCLIV2.msi

Verify in a **new CMD**:
aws --version
```

### 3) Configure AWS credentials

You need an IAM user/role with permissions for:

* CloudFormation, IAM (create roles), API Gateway, Lambda, Step Functions, ECS, ECR, S3, DynamoDB, Textract, CloudWatch Logs

Configure:

```bat
aws configure
```

Confirm identity:

```bat
aws sts get-caller-identity
```

### 4) Set your AWS region

We used:

* `us-west-2`

Set it persistently:

```bat
aws configure set region us-west-2
aws configure get region
```

---

## Environment variables (Windows CMD)

We used these variables throughout:

```bat
set AWS_REGION=us-west-2
for /f "delims=" %i in ('aws sts get-caller-identity --query Account --output text') do set AWS_ACCOUNT_ID=%i

echo %AWS_ACCOUNT_ID%
echo %AWS_REGION%
```

---

## Step 1 — Create ECR repositories (one-time)

If you don’t have permission, you’ll get `AccessDenied`. Ensure your IAM policy allows `ecr:CreateRepository` and `ecr:GetAuthorizationToken`.

Create repos:

```bat
aws ecr create-repository --repository-name splitter --region %AWS_REGION%
aws ecr create-repository --repository-name postprocess --region %AWS_REGION%
```

---

## Step 2 — Login Docker to ECR

This is required before any `docker push`, otherwise you’ll see:

* `no basic auth credentials`

Login:

```bat
aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com
```

Expect:

* `Login Succeeded`

---

## Step 3 — Build and push container images

From the repo root:

```bat
cd C:\path\to\document-parser
```

### Build + push `splitter`

```bat
docker build -t splitter:1 -f splitter\Dockerfile .
docker tag splitter:1 %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/splitter:1
docker push %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/splitter:1
```

### Build + push `postprocess`

```bat
docker build -t postprocess:1 -f postprocess\Dockerfile .
docker tag postprocess:1 %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/postprocess:1
docker push %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/postprocess:1
```

---

## Step 4 — Choose VPC, private subnets, and security group

Fargate tasks need:

* `VpcId`
* `PrivateSubnetIds` (comma-separated)
* `SecurityGroupId`

### 4A) List VPCs

```bat
aws ec2 describe-vpcs --region %AWS_REGION% --query "Vpcs[*].[VpcId,Tags[?Key=='Name']|[0].Value,CidrBlock]" --output table
```

Pick one:

```bat
set VPC_ID=vpc-xxxxxxxx
```

### 4B) List subnets in that VPC

We need **private subnets** (typically `MapPublicIpOnLaunch = False`).

```bat
aws ec2 describe-subnets --region %AWS_REGION% --filters Name=vpc-id,Values=%VPC_ID% --query "Subnets[*].[SubnetId,AvailabilityZone,MapPublicIpOnLaunch]" --output table
```

Pick 2+ subnets (comma-separated):

```bat
set SUBNETS=subnet-aaaaaaa,subnet-bbbbbbb
```

### 4C) Choose a security group

```bat
aws ec2 describe-security-groups --region %AWS_REGION% --filters Name=vpc-id,Values=%VPC_ID% --query "SecurityGroups[*].[GroupId,GroupName,Description]" --output table
```

Pick one:

```bat
set SG_ID=sg-xxxxxxxx
```

Quick sanity:

```bat
echo %VPC_ID%
echo %SUBNETS%
echo %SG_ID%
```

> Note: ECS tasks in private subnets need outbound access to S3/DDB/Textract via **NAT Gateway** or **VPC endpoints**.

---

## Step 5 — Create a CloudFormation artifacts bucket (required for large templates)

If your template is > 51,200 bytes, you’ll see:

* “Templates with a size greater than 51,200 bytes must be deployed via an S3 Bucket.”

Create an artifacts bucket (globally unique):

```bat
set CFN_BUCKET=document-parser-cfn-artifacts-%AWS_ACCOUNT_ID%-usw2
aws s3api create-bucket --bucket %CFN_BUCKET% --region %AWS_REGION% --create-bucket-configuration LocationConstraint=%AWS_REGION%
```

Recommended hardening:

```bat
aws s3api put-public-access-block --bucket %CFN_BUCKET% --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket %CFN_BUCKET% --server-side-encryption-configuration "{\"Rules\":[{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\":\"AES256\"}}]}"
```

If bucket name already exists, use a random suffix:

```bat
set CFN_BUCKET=document-parser-cfn-%AWS_ACCOUNT_ID%-usw2-%RANDOM%
aws s3api create-bucket --bucket %CFN_BUCKET% --region %AWS_REGION% --create-bucket-configuration LocationConstraint=%AWS_REGION%
```

---

## Step 6 — Deploy the CloudFormation stack

Set:

* stack name
* frontend origin (CORS)

```bat
set STACK_NAME=document-parser-prod
set FRONTEND_ORIGIN=https://your-frontend-domain.com
```

Deploy:

```bat
aws cloudformation deploy ^
  --region %AWS_REGION% ^
  --stack-name %STACK_NAME% ^
  --template-file doc-parsing-platform.yml ^
  --s3-bucket %CFN_BUCKET% ^
  --capabilities CAPABILITY_NAMED_IAM ^
  --parameter-overrides ^
    ProjectName=document-parser ^
    Environment=prod ^
    VpcId=%VPC_ID% ^
    PrivateSubnetIds=%SUBNETS% ^
    SecurityGroupId=%SG_ID% ^
    SplitterImage=%AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/splitter:1 ^
    PostProcessorImage=%AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/postprocess:1 ^
    FrontendOrigin=%FRONTEND_ORIGIN%
```

### Get stack outputs

```bat
aws cloudformation describe-stacks --region %AWS_REGION% --stack-name %STACK_NAME% --query "Stacks[0].Outputs" --output table
```

You’ll get values like:

* `ApiBaseUrl`
* `RawBucketName`
* `ParsedBucketName`
* `JobsTableName`
* `StateMachineArn`

---

## Step 7 — test with curl (end-to-end)

Set API base from stack output:

```bat
set API_BASE=https://YOUR_API_ID.execute-api.%AWS_REGION%.amazonaws.com/v1
```

### 7A) Create job → get `jobId` and presigned `upload.url`

```bat
curl -s -X POST "%API_BASE%/jobs" ^
  -H "Content-Type: application/json" ^
  -d "{\"tenantId\":\"t1\",\"filename\":\"sample.pdf\",\"contentType\":\"application/pdf\"}"
```

Set:

```bat
set JOB_ID=PASTE_JOB_ID
set UPLOAD_URL=PASTE_PRESIGNED_URL
```

### 7B) Upload PDF to S3 with presigned PUT

```bat
curl -X PUT "%UPLOAD_URL%" ^
  -H "Content-Type: application/pdf" ^
  --data-binary "@C:\path\to\sample.pdf"
```

### 7C) Start job (kicks Step Functions)

```bat
curl -s -X POST "%API_BASE%/jobs/%JOB_ID%/start"
```

### 7D) Poll job status

```bat
curl -s "%API_BASE%/jobs/%JOB_ID%"
```

### 7E) Get result link and download output

```bat
curl -s "%API_BASE%/jobs/%JOB_ID%/result"
```

If you get a `downloadUrl`:

```bat
curl -L -o document.json "PASTE_DOWNLOAD_URL"
```

---

## Step 8 — test with Python client (optional)

If you have the Python helper script (`submit_job.py`):

Install deps:

```bat
pip install requests
```

Run:

```bat
python submit_job.py --api-base "%API_BASE%" --pdf "C:\path\to\sample.pdf" --tenant-id t1 --out "document.json"
```

---

# Troubleshooting Guide

## A) `docker push ...` → `no basic auth credentials`

Cause: you didn’t login (or login expired)

Fix:

```bat
aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com
```

## B) `aws ecr get-login-password --region %AWS_REGION%` → “Provided region_name '%AWS_REGION%' doesn't match…”

Cause: `%AWS_REGION%` variable is not set (CMD passed it literally)

Fix:

```bat
set AWS_REGION=us-west-2
```

## C) CloudFormation stack fails with `ROLLBACK_COMPLETE`

You cannot update a stack in `ROLLBACK_COMPLETE`. Delete and redeploy:

```bat
aws cloudformation delete-stack --region %AWS_REGION% --stack-name %STACK_NAME%
aws cloudformation wait stack-delete-complete --region %AWS_REGION% --stack-name %STACK_NAME%
```

## D) Step Functions creation fails: “not authorized to create managed-rule”

Cause: Step Functions `.sync` integrations create EventBridge managed rules.

Fix: Add EventBridge permissions to the StepFunctionsRole in the template:

* `events:PutRule`, `events:PutTargets`, `events:DescribeRule`, `events:RemoveTargets`, `events:DeleteRule`, `events:ListTargetsByRule`

Then delete stack (if rollback) and redeploy.

## E) Jobs stuck polling forever

If the state machine errors early (e.g., Choice state references missing input), DynamoDB might never be updated to `FAILED`.

Common example:

* `MaybeSplit` Choice references `$.input.bytes` but `input.bytes` wasn’t passed.

Fixes:

1. Make the Choice state safe using `IsPresent` checks.
2. Ensure StartJob Lambda computes `bytes` (via `head_object`) and passes it into state machine input.
3. Ensure the StartJob Lambda marks job `FAILED` if `StartExecution` fails.

## F) ECS tasks fail to reach AWS services (timeouts / connection errors)

Most common root cause: private subnets without NAT gateway or VPC endpoints.

You need outbound access from the subnets to reach:

* S3, DynamoDB, Textract, Step Functions callbacks, etc.

Solutions:

* Use a NAT gateway in route tables for private subnets
* OR add VPC endpoints (S3 Gateway endpoint is the first one to add)

---

# Useful AWS inspection commands

### Stack events (show failures)

```bat
aws cloudformation describe-stack-events --region %AWS_REGION% --stack-name %STACK_NAME% ^
  --query "StackEvents[?ResourceStatus=='CREATE_FAILED' || ResourceStatus=='UPDATE_FAILED'].[Timestamp,LogicalResourceId,ResourceType,ResourceStatusReason]" ^
  --output table
```

### Step Functions executions

```bat
aws stepfunctions list-executions --region %AWS_REGION% --state-machine-arn YOUR_STATE_MACHINE_ARN --max-results 5
```

### ECS logs (splitter / postprocess)

```bat
aws logs describe-log-streams --region %AWS_REGION% --log-group-name "/document-parser/prod/splitter" --order-by LastEventTime --descending --max-items 5
aws logs get-log-events --region %AWS_REGION% --log-group-name "/document-parser/prod/splitter" --log-stream-name PASTE_STREAM_NAME --limit 200
```

---

# Notes on production readiness

* Consider adding CloudWatch alarms:

  * Step Functions ExecutionsFailed
  * Lambda Errors/Throttles
  * ECS task failures
* Consider WAF / throttling at API Gateway
* Consider per-tenant quotas and idempotency keys for `POST /jobs`

---

```
::contentReference[oaicite:0]{index=0}
```
