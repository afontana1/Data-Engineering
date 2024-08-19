# FastAPI Tutorial

This is a simple example FastAPI application that pretends to be a bookstore.

# Deploying FastAPI to AWS Lambda

We'll need to modify the API so that it has a Lambda handler. But after that, we can zip
up the dependencies like this:

```bash
pip install -t lib -r requirements.txt
```

Now you'll need to create a zip file where the FastAPI app and the dependencies are in the 
same closure.

```
(cd lib; zip ../lambda_function.zip -r .)
```

Now add our FastAPI file.

```
zip lambda_function.zip -u main.py
```