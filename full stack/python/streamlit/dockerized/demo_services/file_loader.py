from configparser import ConfigParser
import boto3
import streamlit as st


class boto3_setup():
  def __init__(self, bucket):
        self.bucket = bucket

  def s3_client(self, access_key, access_secret):
      client = boto3.client(
              's3',
              aws_access_key_id= access_key,
              aws_secret_access_key= access_secret
      )
      return client

class widget_process():
  def __init__(self):
    self.access_key = st.text_input(label='access_key')
    self.access_secret = st.text_input(label='secret')
    self.bucket = st.text_input(label='Bucket Name')
    self.file_name = st.text_input(label='file_name')
    self.setup = boto3_setup(self.bucket)

  def read_file(self):
        client = self.setup.s3_client(self.access_key, self.access_secret)
        try:
          response = client.get_object(Bucket=self.bucket, Key=self.file_name)
          contents = response['Body']
        except Exception as e:
          print("File read failed due to exceptiion {}".format(e))
        return contents

  def list_bucket(self):
        client = self.setup.s3_client(self.access_key, self.access_secret)
        try:
          response = client.list_objects_v2(Bucket=self.bucket)
        except Exception as e:
          print("File list failed due to exceptiion {}".format(e))
        return response['Contents']