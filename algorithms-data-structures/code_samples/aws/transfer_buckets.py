import json
from config import config
import boto3
import botocore

from typing import Optional
from collections import OrderedDict

import logging
from io import BytesIO
import multiprocessing
import threading

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Struct:
    """The recursive class for building and representing objects with."""

    def __init__(self, obj):
        for k, v in obj.items():
            if isinstance(v, dict):
                setattr(self, k, Struct(v))
            elif isinstance(v, (tuple, list)):
                setattr(self, k, [Struct(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, v)

    def __getitem__(self, val):
        return self.__dict__[val]

    def __repr__(self):
        return "{%s}" % str(
            ", ".join("%s : %s" % (k, repr(v)) for (k, v) in self.__dict__.items())
        )


class FileTransferClient(object):
    """
    Class to move any object or collection of objects from one
    S3 bucket to another. The object will be initialized with
    source location, target location, and file name.

    Option to move all objects with particular extenions.
    """

    def __init__(
        self,
        source: str = "",
        target: str = "",
        extensions: Optional[list[str]] = None,
        **kwargs
    ):
        """initialize object with source and target."""
        self.source = source
        self.target = target
        self.extensions = extensions
        self.filename = kwargs.get("filename", None)

        if not kwargs.get("client", None):
            self.session = boto3.resource("s3")
        else:
            self.session = kwargs.get("client")

    @classmethod
    def no_client(cls, **kwargs):
        """Class instance without using client.

        Args:
                1. source
                2. target
        """
        if (not kwargs.get("source", None)) or (not kwargs.get("target", None)):
            raise Exception("Invalid Parameters")

        return cls(
            source=kwargs["source"],
            target=kwargs["target"],
            filename=kwargs.get("filename", None),
            extensions=kwargs.get("extensions", None),
        )

    @classmethod
    def from_client(cls, **kwargs):
        """Class instance for S3 client.

        Args: S3 Client credentials.
                1. access_key_id
                2. secret_access_key
                3. region
        """

        source = kwargs.get("source", None)
        target = kwargs.get("target", None)
        filename = kwargs.get("filename", None)

        if (not source) and (not target):
            raise ("Provide target and source destination")

        access_id = kwargs.get("access_id", None)
        secret_key = kwargs.get("secret_key", None)
        region = kwargs.get("region", None)

        if (not access_id) or (not secret_key):
            raise Exception("Provide the correct credentials")

        client = boto3.client(
            "s3",
            aws_access_key_id=access_id,
            aws_secret_access_key=secret_key,
            region_name=region if region else "us-west-2",
        )

        return cls(
            source=source,
            target=target,
            extensions=kwargs.get("extensions", None),
            filename=filename,
            client=client,
        )


class TransferBuckets(FileTransferClient):
    """Interface for transferring files."""

    def __init__(
        self,
        source: str = "",
        target: str = "",
        extensions: Optional[list[str]] = None,
        **kwargs
    ):
        super(TransferBuckets, self).__init__(source, target, extensions, **kwargs)
        self.methods = self._get_methods()

    def _get_methods(self):
        methods = sorted(
            [
                func
                for func in dir(self)
                if callable(getattr(self, func))
                and func.startswith(self._determine_method())
            ]
        )
        method_tokens = [method.split("_")[2] for method in methods]
        return dict(zip(method_tokens, methods))

    def _determine_method(self):
        """Determine if client or session"""
        if isinstance(self.__dict__.get("session"), botocore.client.BaseClient):
            return "_client"
        elif isinstance(
            self.__dict__.get("session"), boto3.resources.base.ServiceResource
        ):
            return "_session"
        else:
            return

    @property
    def set_buckets_and_paths(self):

        buckets_and_paths = OrderedDict(
            [
                ("_in_bucket", self.source.split("/")[0]),
                ("_out_bucket", self.target.split("/")[0]),
                ("_in_path", "/".join(self.source.split("/")[1:])),
                ("_out_path", "/".join(self.target.split("/")[1:])),
            ]
        )
        self.buckets_and_paths = buckets_and_paths
        return buckets_and_paths

    def _client_get_bucket(self, bucket, path):
        """get files from bucket using client"""
        paginator = self.session.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=path)

        for page in pages:
            if "Contents" in page:

                if (not self.filename) and (not self.extensions):
                    for file_obj in page["Contents"]:
                        yield Struct(file_obj)

                elif self.filename:
                    print("in filename")
                    for file_obj in page["Contents"]:
                        file_object = Struct(file_obj)
                        fname = file_object.Key.split("/")[-1]
                        if fname == self.filename:
                            yield file_object

                elif self.extensions:
                    print("in extensions")
                    for file_obj in page["Contents"]:
                        file_object = Struct(file_obj)
                        extension = file_object.Key.split(".")
                        if not extension:
                            continue
                        if extension[-1] in self.extensions:
                            yield file_object

    def _client_write_to_bucket(self, bucket, path, iterator_of_files):
        """upload file to s3"""
        for file_obj in iterator_of_files:

            file_path = file_obj.Key.split(".")
            if len(file_path) < 2:
                continue

            file_object = Struct(
                self.session.get_object(
                    Bucket=self.buckets_and_paths["_in_bucket"], Key=file_obj.Key
                )
            )

            print(file_object)

            try:
                print(bucket, path + file_obj.Key.split("/")[-1])
                response = self.session.put_object(
                    Bucket=bucket,
                    Body=file_object.Body.read(),
                    Key=path + file_obj.Key.split("/")[-1],
                )
            except Exception as e:
                print(e)
                logger.info("Error putting file in S3,file: {}".format(file_obj.Key))
        return True

    def _session_put(self, data, bucket, key):
        """wrapper for s3 session"""
        self.session.meta.client.upload_fileobj(data, Bucket=bucket, Key=key)

    def _session_get_bucket(self, bucket, path):
        """get content from bucket"""
        in_bucket = self.session.Bucket(bucket)
        file_objs = in_bucket.objects.filter(Prefix=path).all()

        if (not self.extensions) and (not self.filename):
            for file_obj in file_objs:
                yield file_obj

        if self.filename:
            for file_obj in file_objs:
                if file_obj.key == self.filename:
                    yield file_obj

        if self.extensions:
            for file_obj in file_objs:
                if file_obj.key.split(".")[-1] in self.extensions:
                    yield file_obj

    def _session_write_to_bucket(self, bucket, path, iterator_of_files):
        """write content to bucket"""
        processes = []
        for file_obj in iterator_of_files:

            file_path = file_obj.key.split(".")
            if len(file_path) < 2:
                continue

            file_object = Struct(
                self.session.Object(
                    bucket_name=self.buckets_and_paths["_in_bucket"], key=file_obj.key
                ).get()
            )
            print(file_object)
            process = multiprocessing.Process(
                target=self._session_put,
                args=(
                    BytesIO(file_object.Body.read()),
                    bucket,
                    path + file_obj.key.split("/")[-1],
                ),
            )
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        return True

    def transfer_files(self):
        """Main entry point"""
        buckets_and_paths = self.set_buckets_and_paths

        file_generator = getattr(self, self.methods.get("get"))(
            bucket=buckets_and_paths["_in_bucket"], path=buckets_and_paths["_in_path"]
        )

        response = getattr(self, self.methods.get("write"))(
            bucket=buckets_and_paths["_out_bucket"],
            path=buckets_and_paths["_out_path"],
            iterator_of_files=file_generator,
        )

        return {"status": 200 if response else 202}


def lambda_handler(event, context):
    print(event)

    SOURCE_LOCATION = ""
    TARGET_LOCATION = ""

    event_information = event.get("Records")[0].get("object")
    # fname = event_information.get("key") ##OPTIONAL PARAM TO PASS

    logger.info("Instantiating client.")

    file_transfer_object = TransferBuckets.no_client(
        source=SOURCE_LOCATION,
        target=TARGET_LOCATION,
        extensions=["csv"],
        filename=None,
    )

    logger.info("Created file transfer object")
    response = file_transfer_object.transfer_files()

    return {"statusCode": 200, "body": json.dumps(response)}
