import boto3
import botocore
import gzip
import json
import os
import yaml
import sys

from io import BytesIO, StringIO
from pathlib import Path
from typing import Union

from datetime import datetime
import json


class SelectQuerySet:
    """
    Iterator for fetching select query results in chunks.
    The following example uses the select queryset along with JsonNlSplitFileWriter to
    write the contents of a table to s3 in .jsonl.gz
    con = cx_Oracle.connect(
        parameters['DB_USER_ID'],
        parameters['DB_PWD'],
        parameters['DB_DSN']
    )
    select_queryset = SelectQuerySet(
        con.cursor(),
        "select * from table",
        1000,
    )
    # Write out json string
    with JsonNlSplitFileWriter("s3://test/test-file.jsonl.gz") as writer:
        column_names = select_queryset.headers
        for row in select_queryset:
            json_line_str = json.dumps(
                dict(zip(column_names, row)),
                cls=DateTimeEncoder
            )
            writer.write_line(json_line_str)
    # Use a function to convert row to json
    with JsonNlSplitFileWriter("s3://test/test-file.jsonl.gz") as writer:
        column_names = select_queryset.headers
        def transform_line(row):
            return json.dumps(dict(zip(column_names, row)), cls=DateTimeEncoder)
        select_queryset.write_to_file(writer, transform_line)
    # Use a function to convert row to json but write multiple lines at once
    with JsonNlSplitFileWriter("s3://test/test-file.jsonl.gz") as writer:
        column_names = select_queryset.headers
        def transform_line(row):
            return json.dumps(dict(zip(column_names, row)), cls=DateTimeEncoder)
        for results in select_queryset.iter_chunks():
            writer.write_lines(results, transform_line)
    """

    def __init__(self, cursor, select_query, fetch_size=1000, **query_kwargs):
        """
        Sets the curser, query and executes
        :param cursor: curser object: such as cx_Oracle.connect().cursor
        :param select_query: string: "select * from table"
        :param fetch_size: int: 1000
        :param query_kwargs: kwargs: kwargs for query formatting
        """
        self.query = select_query
        self.cursor = cursor
        self.cursor.arraysize = fetch_size
        self.fetch_size = fetch_size
        self.cursor.execute(select_query, **query_kwargs)

    def __iter__(self):
        """Reset iterator and n to 0"""
        for r in self.cursor:
            yield r

    def iter_chunks(self):
        results = self.cursor.fetchmany(self.fetch_size)
        while results:
            yield results
            try:
                results = self.cursor.fetchmany(self.fetch_size)
            except Exception:
                results = None
                break

    @property
    def headers(self):
        """Return column names"""
        return [c[0] for c in self.cursor.description]

    def write_to_file(self, file_writer, line_transform=lambda x: x):
        for results in self.iter_chunks():
            file_writer.write_lines(results, line_transform)


class DateTimeEncoder(json.JSONEncoder):
    """
    Json encoder that handles datetime objects and formats them to iso format.
    json_dict = {
        "datetime": datetime(2111, 1, 1, 1, 1, 1),
        "a": "b"
    }
    json_str = json.dumps(json_dict, cls=DateTimeEncoder)
    """

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def gzip_string_write_to_s3(file_as_string, s3_path):
    """
    Writes IoString to s3 path as gziped output
    :param file_as_string: IOString
    :param s3_path: "s3://....
    :return:
    """
    s3_resource = boto3.resource("s3")
    b, k = s3_path_to_bucket_key(s3_path)
    compressed_out = gzip.compress(bytes(file_as_string, "utf-8"))
    s3_resource.Object(b, k).put(Body=compressed_out)


def s3_path_to_bucket_key(s3_path):
    """
    Splits out s3 file path to bucket key combination
    """
    return s3_path.replace("s3://", "").split("/", 1)


def bucket_key_to_s3_path(bucket, key):
    """
    Takes an S3 bucket and key combination and returns the
    full S3 path to that location.
    """
    return f"s3://{bucket}/{key}"


def _add_slash(s):
    """
    Adds slash to end of string
    """
    return s if s[-1] == "/" else s + "/"


def get_filepaths_from_s3_folder(
    s3_folder_path, file_extension=None, exclude_zero_byte_files=True
):
    """
    Get a list of filepaths from a bucket. If extension is set to a string
    then only return files with that extension otherwise if set to None (default)
    all filepaths are returned.
    :param s3_folder_path: "s3://...."
    :param extension: file extension, e.g. .json
    :param exclude_zero_byte_files: Whether to filter out results of zero size: True
    :return: A list of full s3 paths that were in the given s3 folder path
    """

    s3_resource = boto3.resource("s3")

    if file_extension is not None:
        if file_extension[0] != ".":
            file_extension = "." + file_extension

    # This guarantees that the path the user has given is really a 'folder'.
    s3_folder_path = _add_slash(s3_folder_path)

    bucket, key = s3_path_to_bucket_key(s3_folder_path)

    s3b = s3_resource.Bucket(bucket)
    obs = s3b.objects.filter(Prefix=key)

    if file_extension is not None:
        obs = [o for o in obs if o.key.endswith(file_extension)]

    if exclude_zero_byte_files:
        obs = [o for o in obs if o.size != 0]

    ob_keys = [o.key for o in obs]

    paths = sorted([bucket_key_to_s3_path(bucket, o) for o in ob_keys])

    return paths


def get_object_body(s3_path: str, encoding: str = "utf-8") -> str:
    """
    Gets object body from file in S3
    :param s3_path: "s3://...."
    :param encoding: File type encoding (utf-8 default)
    :return: decoded string data from S3
    """
    s3_resource = boto3.resource("s3")
    bucket, key = s3_path_to_bucket_key(s3_path)
    obj = s3_resource.Object(bucket, key)
    text = obj.get()["Body"].read().decode(encoding)
    return text


def read_json_from_s3(s3_path: str, encoding: str = "utf-8", *args, **kwargs) -> dict:
    """
    Reads a json from the provided s3 path
    :param s3_path: "s3://...."
    :param encoding: File type encoding (utf-8 default)
    :param *args: Passed to json.loads call
    :param **kwargs: Passed to json.loads call
    :return: data from the json
    """
    text = get_object_body(s3_path, encoding)
    return json.loads(text, *args, **kwargs)


def write_json_to_s3(data, s3_path, *args, **kwargs):
    """
    Writes a json to the provided s3 path
    :param data: data to be written to a json file
    :param s3_path: "s3://...."
    :param *args: Passed to json.dump call
    :param **kwargs: Passed to json.dump call
    :return: response dict of upload to s3
    """
    bucket, key = s3_path_to_bucket_key(s3_path)
    s3_resource = boto3.resource("s3")
    log_file = StringIO()
    json.dump(data, log_file, *args, **kwargs)
    log_obj = s3_resource.Object(bucket, key)
    log_upload_resp = log_obj.put(Body=log_file.getvalue())
    return log_upload_resp


def read_yaml_from_s3(s3_path: str, encoding: str = "utf-8", *args, **kwargs) -> dict:
    """
    Reads a yaml file from the provided s3 path
    :param s3_path: "s3://...."
    :param encoding: File type encoding (utf-8 default)
    :param *args: Passed to yaml.safe_load call
    :param **kwargs: Passed to yaml.safe_load call
    :return: data from the yaml
    """
    text = get_object_body(s3_path, encoding)
    return yaml.safe_load(text, *args, **kwargs)


def copy_s3_folder_contents_to_new_folder(
    from_s3_folder_path, to_s3_folder_path, exclude_zero_byte_files=False
):
    """
    Copies complete folder structure within from_s3_folder_path
    to the to_s3_folder_path.
    Note any s3 objects in the destination folder will be overwritten if it matches the
    object name being written.
    :param from_s3_folder_path: Folder path that you want to copy "s3://...."
    :param to_s3_folder_path: Folder path that you want to write contents to "s3://...."
    """
    from_s3_folder_path = _add_slash(from_s3_folder_path)
    to_s3_folder_path = _add_slash(to_s3_folder_path)

    all_from_filepaths = get_filepaths_from_s3_folder(
        from_s3_folder_path, exclude_zero_byte_files=exclude_zero_byte_files
    )
    for afp in all_from_filepaths:
        tfp = afp.replace(from_s3_folder_path, to_s3_folder_path)
        copy_s3_object(afp, tfp)


def delete_s3_object(s3_path):
    """
    Deletes the file at the s3_path given.
    :param s3_path: "s3://...."
    """
    s3_resource = boto3.resource("s3")
    b, o = s3_path_to_bucket_key(s3_path)
    s3_resource.Object(b, o).delete()


def delete_s3_folder_contents(s3_folder_path, exclude_zero_byte_files=False):
    """
    Deletes all files within the s3_folder_path given given.
    :param s3_folder_path: Folder path that you want to delete "s3://...."
    :param exclude_zero_byte_files: Whether to filter out results of zero size: False
    """
    s3_folder_path = _add_slash(s3_folder_path)
    all_filepaths = get_filepaths_from_s3_folder(
        s3_folder_path, exclude_zero_byte_files=exclude_zero_byte_files
    )
    for f in all_filepaths:
        delete_s3_object(f)


def copy_s3_object(from_s3_path, to_s3_path):
    """
    Copies a file in S3 from one location to another.
    Automatically overwrites to_s3_path if already exists.
    :param from_s3_path: S3 path that you want to copy "s3://...."
    :param to_s3_path: S3 destination path "s3://...."
    """
    s3_resource = boto3.resource("s3")
    to_bucket, to_key = s3_path_to_bucket_key(to_s3_path)
    if "s3://" in from_s3_path:
        from_s3_path = from_s3_path.replace("s3://", "")
    s3_resource.Object(to_bucket, to_key).copy_from(CopySource=from_s3_path)


def check_for_s3_file(s3_path):
    """
    Checks if a file exists in the S3 path provided.
    :param s3_path: "s3://...."
    :returns: Boolean stating if file exists in S3
    """
    # Taken from:
    # https://stackoverflow.com/questions/33842944/check-if-a-key-exists-in-a-bucket-in-s3-using-boto3
    s3_resource = boto3.resource("s3")
    bucket, key = s3_path_to_bucket_key(s3_path)
    try:
        s3_resource.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise
    else:
        # The object does exist.
        return True


def write_local_file_to_s3(local_file_path, s3_path, overwrite=False):
    """
    Copy a file from a local folder to a location on s3.
    :param local_file_path: "myfolder/myfile.json"
    :param s3_path: "s3://path/to/myfile.json"
    :returns: s3_resource response
    """

    bucket, key = s3_path_to_bucket_key(s3_path)
    s3_resource = boto3.resource("s3")

    if check_for_s3_file(s3_path) and overwrite is False:
        raise ValueError("File already exists.  Pass overwrite = True to overwrite")
    else:
        resp = s3_resource.meta.client.upload_file(local_file_path, bucket, key)

    return resp


def write_local_folder_to_s3(
    root_folder: Union[Path, str],
    s3_path: str,
    overwrite: bool = False,
    include_hidden_files: bool = False,
) -> None:
    """Copy a local folder and all its contents to s3, keeping its directory structure.
    :param root_folder: the folder whose contents you want to upload
    :param s3_path: where you want the folder to be located when it's uploaded
    :param overwrite: if True, overwrite existing files in the target location
        if False, raise ValueError if existing files are found in the target location
    :param include_hidden_files: if False, ignore files whose names start with a .
    :returns: None
    """
    for obj in Path(root_folder).rglob("*"):
        if obj.is_file() and (include_hidden_files or not obj.name.startswith(".")):
            # Construct s3 path based on current filepath and local root folder
            relative_to_root = str(obj.relative_to(root_folder))
            file_s3_path = os.path.join(s3_path, relative_to_root)
            write_local_file_to_s3(str(obj), file_s3_path, overwrite)


def write_s3_file_to_local(
    s3_path: str,
    local_file_path: Union[Path, str],
    overwrite: bool = False,
) -> None:
    """Save a file from an s3 path to a local folder.
    :param s3_path: full s3 path of the file you want to download
    :param local_file_path: Path or str for where to save the file
    :param overwrite: if True, overwrite an existing file at the local_file_path
    :returns: None
    """
    # Check if there's already a file there
    if not overwrite:
        location = Path(local_file_path)
        if location.is_file():
            raise FileExistsError(
                (
                    f"There's already a file at {str(location)}. "
                    "Set overwrite to True to replace it."
                )
            )

    # Create the folder if it doesn't yet exist
    folder = str(local_file_path).rsplit("/", 1)[0]
    Path(folder).mkdir(parents=True, exist_ok=True)

    # Download the file
    s3_client = boto3.client("s3")
    bucket, key = s3_path_to_bucket_key(s3_path)
    s3_client.download_file(bucket, key, str(local_file_path))


def write_s3_folder_to_local(
    s3_path: str, local_folder_path: Union[Path, str], overwrite: bool = False
) -> None:
    """Copy files from an s3 'folder' to a local folder, keeping directory structure.
    :param s3_path: full s3 path of the folder whose contents you want to download
    :param local_folder_path: Path or str for where to save the contents of s3_path
    :param overwrite: if False, raise an error if any of the files already exist
    :returns: None
    """
    # Prepare local root folder
    root = Path(local_folder_path)
    root.mkdir(parents=True, exist_ok=True)

    # Get an object representing the bucket
    s3_resource = boto3.resource("s3")
    bucket_name, s3_folder = s3_path_to_bucket_key(s3_path)
    bucket = s3_resource.Bucket(bucket_name)

    # For each file in bucket, check if it needs a new subfolder, then download it
    for obj in bucket.objects.filter(Prefix=s3_folder):
        # Split up s3 path to work out directory structure for the local file
        s3_subfolder, filename = obj.key.rsplit("/", 1)
        local_subfolder = root / s3_subfolder
        destination = local_subfolder / filename

        # Raise an error if file already exists and not overwriting
        if not overwrite and destination.is_file():
            raise FileExistsError(
                (
                    f"There's already a file at {str(destination)}. "
                    "Set overwrite to True to replace it."
                )
            )

        # Make the local folder if it doesn't exist, then download the file
        local_subfolder.mkdir(parents=True, exist_ok=True)
        bucket.download_file(obj.key, str(destination))


class BaseSplitFileWriter:
    """
    Base class for splitting large datasets in to chunks and writing to s3.
    This is acts as a "file like object". Data is written to an in memory file
    (note this file is defined in subclasses and not set in this base class).
    until it hits a max_bytes limit at which point the data is written to S3
    as single file. The in memory file is defined by the sub classes
    BytesSlitFileWriter and StringSplitFileWriter. These subclasses attempt
    to mimic the expected response of BytesIO and StringIO.
    :param s3_basepath: The base path to the s3 location you want to write to S3://...
    :param filename_prefix: The filename that you want to keep constant. Every written
    file is prefixed with this string.
    S3 objects written will end in the file number and the extension.
    :param max_bytes: The maximum number of bytes for each file (uncompressed file size)
        default set at 1GB.
    :param compress_on_upload: If the file should be compressed before writing to S3
        (default True). Note does not affect the file_extension parameter.
    :param file_extension: String representing the file extension.
        Should not be prefixed with a '.'.
    """

    def __init__(
        self,
        s3_basepath,
        filename_prefix,
        max_bytes=1000000000,
        compress_on_upload=True,
        file_extension=None,
    ):
        self.filename_prefix = filename_prefix
        self.s3_basepath = s3_basepath
        self.max_bytes = max_bytes
        self.num_files = 0
        self.mem_file = None
        self.compress_on_upload = compress_on_upload
        self.file_extension = "" if file_extension is None else file_extension
        self.mem_file = self.get_new_mem_file()

    def __enter__(self):
        self.mem_file = self.get_new_mem_file()
        self.num_files = 0
        return self

    def __exit__(self, *args):
        self.close()

    def get_new_mem_file(self):
        """
        Overwritten by subclasses. Should return a filelike object.
        """
        return ""

    def _compress_data(self, data):
        """
        Can be overwritten by subclasses. Should return compressed data.
        """
        return gzip.compress(data)

    def write(self, b):
        self.mem_file.write(b)
        if self.file_size_limit_reached():
            self.write_to_s3()

    def writelines(self, lines):
        self.mem_file.writelines(lines)
        if self.file_size_limit_reached():
            self.write_to_s3()

    def file_size_limit_reached(self):
        if (self.max_bytes) and (self.mem_file.tell() > self.max_bytes):
            return True
        else:
            return False

    def write_to_s3(self):
        s3_resource = boto3.resource("s3")
        b, k = s3_path_to_bucket_key(self.get_s3_filepath())
        data = self.mem_file.getvalue()
        if self.compress_on_upload:
            data = self._compress_data(data)

        s3_resource.Object(b, k).put(Body=data)

        self.reset_file_buffer()

    def reset_file_buffer(self):
        self.num_files += 1
        self.mem_file.close()
        self.mem_file = self.get_new_mem_file()

    def get_s3_filepath(self):
        fn = f"{self.filename_prefix}-{self.num_files}.{self.file_extension}"
        return os.path.join(self.s3_basepath, fn)

    def close(self):
        """Write all remaining lines to a final file"""
        if self.mem_file.tell():
            self.write_to_s3()
            self.mem_file.close()


class BytesSplitFileWriter(BaseSplitFileWriter):
    """
     BytesIO file like object for splitting large datasets in to chunks and
     writing to s3. Data is written to a BytesIO file buffer until it hits a
     max_bytes limit at which point the data is written to S3 as a
     as single file. Then data continues to be written to a new BytesIO buffer until that
     hits the size limit which results in a new single file being written to S3. Each S3
     file is suffixed with an integer (first file is suffixed with 0, the next 1, etc)
     :param s3_basepath: The base path to the s3 location you want to write to S3://...
     :param filename_prefix: The filename that you want to keep constant. Every written
         file is prefixed with this string.
     S3 objects written will end in the file number and the extension.
     :param max_bytes: The maximum number of bytes for each file (uncompressed file size)
         default set at 1GB.
     :param compress_on_upload: If the file should be compressed before writing to S3
         (default True). Note does not affect the file_extension parameter.
     :param file_extension: String representing the file extension.
         Should not be prefixed with a '.'.
    :Example:
     # Example 1 - Uploads bytes text to S3
     # The following example would write the two text strings
     # to two files:
     # s3://test/folder/test-file-0.txt and s3://test/folder/test-file-1.txt
     # as each write exceeds the max_bytes limit
     from dataengineeringutils3.writer import BytesSplitFileWriter
     with BytesSplitFileWriter("s3://test/folder/",
         "test-file",
         max_bytes=50,
         compress_on_upload=False,
         file_extension="txt"
     ) as f:
         f.write(b"This is some text")
         f.write(b"This is some other text")
     # Example 2 - Using it with a writing package
     # The following example uses jsonlines to write the data to a BytesSplitFileWriter
     # when data written to the in memory buffer exceeds BytesSplitFileWriter then the
     # data in the buffer is written to S3. With the first file being
     # "s3://test/folder/test-file-0.jsonl.gz"
     # and the next "s3://test/folder/test-file-1.jsonl.gz", etc.
     from dataengineeringutils3.writer import BytesSplitFileWriter
     from jsonlines import Writer
     test_data = [
         {"col1": 0, "col2": "x"},
         {"col1": 1, "col2": "y"},
         {"col1": 2, "col2": "z"}
     ]
     bsfw = BytesSplitFileWriter("s3://test/folder/",
         "test-file",
         max_bytes=30,
         compress_on_upload=True,
         file_extension="jsonl.gz"
     )
     # Same functionality as passing BytesIO() file into the jsonlines.Writer
     json_writer = Writer(bsfw)
     json_writer.write_all(test_data)
     json_writer.close()
     # Closing the objects sends off the remaining data in the io buffer.
     # closing is required in this example as jsonlines.Writer doesn't close
     # the bytesFile as it was opened before being passed to the Writer
     bsfw.close()
    """

    def get_new_mem_file(self):
        return BytesIO()


class StringSplitFileWriter(BaseSplitFileWriter):
    """
     StringIO file like object for splitting large datasets in to chunks and
     writing to s3. Data is written to a StringIO file buffer until it hits a
     max_bytes limit at which point the data is written to S3 as a
     as single file. Then data continues to be written to a new StringIO buffer
     until that hits the size limit which results in a new single file being
     written to S3. Each S3 file is suffixed with an integer (first file is
     suffixed with 0, the next 1, etc)
     :param s3_basepath: The base path to the s3 location you want to write to S3://...
     :param filename_prefix: The filename that you want to keep constant. Every written
         file is prefixed with this string.
     S3 objects written will end in the file number and the extension.
     :param max_bytes: The maximum number of bytes for each file (uncompressed file size)
         default set at 1GB.
     :param compress_on_upload: If the file should be compressed before writing to S3
         (default True). Note does not affect the file_extension parameter.
     :param file_extension: String representing the file extension. Should not be
         prefixed with a '.'.
    :Example:
     # Example 1 - Uploads bytes text to S3
     # The following example would write the two text strings
     # to two files:
     # s3://test/folder/test-file-0.txt and s3://test/folder/test-file-1.txt
     # as each write exceeds the max_bytes limit
     from dataengineeringutils3.writer import StringSplitFileWriter
     with StringSplitFileWriter("s3://test/folder/",
         "test-file",
         max_bytes=50,
         compress_on_upload=False,
         file_extension="txt"
     ) as f:
         f.write("This is some text")
         f.write("This is some other text")
     # Example 2 - Using it with a writing package
     # The following example uses jsonlines to write the
     # data to a BytesSplitFileWriter
     # when data written to the in memory buffer exceeds
     # BytesSplitFileWriter then the data in the buffer
     # is written to S3. With the first file being
     # "s3://test/folder/test-file-0.jsonl.gz"
     # and the next "s3://test/folder/test-file-1.jsonl.gz", etc.
     from dataengineeringutils3.writer import StringSplitFileWriter
     from jsonlines import Writer
     test_data = [
         {"col1": 0, "col2": "x"},
         {"col1": 1, "col2": "y"},
         {"col1": 2, "col2": "z"}
     ]
     ssfw = StringSplitFileWriter("s3://test/folder/",
         "test-file",
         max_bytes=30,
         compress_on_upload=True,
         file_extension="jsonl.gz"
     )
     # Same functionality as passing BytesIO() file into the jsonlines.Writer
     json_writer = Writer(ssfw)
     json_writer.write_all(test_data)
     json_writer.close()
     # Closing the objects sends off the remaining data in the io buffer.
     # closing is required in this example as jsonlines.Writer doesn't close
     # the bytesFile as it was opened before being passed to the Writer
     ssfw.close()
    """

    def get_new_mem_file(self):
        return StringIO()

    def _compress_data(self, data):
        """
        Converts string data to bytes and then compresses
        """
        return gzip.compress(bytes(data, "utf-8"))


class JsonNlSplitFileWriter(BaseSplitFileWriter):
    """
    Class for writing json line into large datasets in to chunks and writing to s3.
    This class writes to a string (rather than fileIO) and does smaller checks for
    a speedier read write. Espeicially when writing multiple lines. However,
    if scaling to large amounts of data it is probably better to use a json writer
    like jsonlines with the BytesSplitFileWriter. The extension and the _write
    methods are defined in classes which extend this class
    lines = [
        '{"key": "value"}'
    ]
    with JsonNlSplitFileWriter("s3://test/", "test-file") as writer:
        for line in lines:
            writer.write_line(line)
    """

    def __init__(
        self, s3_basepath, filename_prefix, max_bytes=1000000000, chunk_size=1000
    ):
        super(JsonNlSplitFileWriter, self).__init__(
            s3_basepath=s3_basepath,
            filename_prefix=filename_prefix,
            max_bytes=max_bytes,
            compress_on_upload=True,
            file_extension="jsonl.gz",
        )

        self.chunk_size = chunk_size
        self.total_lines = 0
        self.num_lines = 0

    def __enter__(self):
        self.mem_file = self.get_new_mem_file()
        self.num_lines = 0
        self.num_files = 0
        return self

    def __exit__(self, *args):
        self.close()

    def write_line(self, line):
        """Writes line as string"""
        self.mem_file += f"{line}\n"
        self.num_lines += 1
        self.total_lines += 1
        if self.file_size_limit_reached():
            self.write_to_s3()

    def file_size_limit_reached(self):
        limit_met = sys.getsizeof(self.mem_file) > self.max_bytes

        if not limit_met and self.chunk_size:
            return self.num_lines >= self.chunk_size
        else:
            return limit_met

    def write_lines(self, lines, line_transform=lambda x: x):
        """
        Writes multiple lines then checks if file limit hit.
        So will be quicker but less accurate on breaking up files.
        """
        self.mem_file += "\n".join(line_transform(line) for line in lines) + "\n"
        self.num_lines += len(lines)
        self.total_lines += len(lines)
        if self.file_size_limit_reached():
            self.write_to_s3()

    def reset_file_buffer(self):
        self.num_files += 1
        self.num_lines = 0
        self.mem_file = self.get_new_mem_file()

    def write_to_s3(self):
        gzip_string_write_to_s3(self.mem_file, self.get_s3_filepath())
        self.reset_file_buffer()

    def close(self):
        """Write all remaining lines to a final file"""
        if self.num_lines:
            self.write_to_s3()
