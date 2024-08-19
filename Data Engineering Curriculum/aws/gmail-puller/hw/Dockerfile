FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]
