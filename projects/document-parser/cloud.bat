set STACK_NAME=document-parser-prod
set FRONTEND_ORIGIN=https://your-frontend-domain.com

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
    SplitterImage=%AWS_ACCOUNT_ID%.dkr.ecr.us-west-2.amazonaws.com/splitter:1 ^
    PostProcessorImage=%AWS_ACCOUNT_ID%.dkr.ecr.us-west-2.amazonaws.com/postprocess:1 ^
    FrontendOrigin=%FRONTEND_ORIGIN%