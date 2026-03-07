import asyncio
import math
import os

import aiobotocore
import aiofiles

AWS_S3_HOST = ""
AWS_SECRET_ACCESS_KEY = "SECRET_KEY"
AWS_ACCESS_KEY_ID = "ACCESS_KEY"
AWS_MULTIPART_BYTES_PER_CHUNK = 10000000  # ~ 6mb
AWS_S3_BUCKET_NAME = "test"

# We have to keep info about uploaded parts.
# https://github.com/boto/boto3/issues/50#issuecomment-72079954
part_info = {"Parts": []}
# File object is distributed across coroutines
# and the async file library is using threads under the hood.
# This might create data races with unpredictable issues
file_shared_lock = asyncio.Lock()


async def upload_chunk(
    client, file, upload_id, chunk_number, bytes_per_chunk, source_size, key
):
    offset = chunk_number * bytes_per_chunk
    remaining_bytes = source_size - offset
    bytes_to_read = min([bytes_per_chunk, remaining_bytes])
    part_number = chunk_number + 1

    async with file_shared_lock:
        await file.seek(offset)
        chunk = await file.read(bytes_to_read)

    # Step 2 - upload part
    # Important args:
    # 	Bucket     - bucket name where file will be stored;
    # 	Body 	   - chunk data in bytes;
    # 	UploadId   - id of the multipart upload which identifies uploading file;
    # 	PartNumber - number which identifies a chunk of data;
    # 	Key        - path in S3 under which the file will be available;
    # Important response attributes:
    # 	ETag 	   - identifier of the file representing its version;
    resp = await client.upload_part(
        Bucket=AWS_S3_BUCKET_NAME,
        Body=chunk,
        UploadId=upload_id,
        PartNumber=part_number,
        Key=key,
    )

    global part_info
    part_info["Parts"].append({"PartNumber": part_number, "ETag": resp["ETag"]})


async def begin_multipart_upload(
    from_local_path,
    to_s3_folder_path,
    host=AWS_S3_HOST,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    bytes_per_chunk=AWS_MULTIPART_BYTES_PER_CHUNK,
):
    filename = os.path.basename(from_local_path)
    key = "{}/{}".format(to_s3_folder_path, filename)

    session = aiobotocore.get_session()
    async with session.create_client(
        "s3",
        endpoint_url=host,
        aws_secret_access_key=aws_secret_access_key,
        aws_access_key_id=aws_access_key_id,
    ) as client:
        source_size = os.stat(from_local_path).st_size
        chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))
        print("chunks_count: ", chunks_count)

        # Step 1 - create multipart upload
        # Important args:
        # 	Bucket     - bucket name where file will be stored;
        # 	Key        - path in S3 under which the file will be available
        # 	Expires    - when uploaded parts will be deleted if multipart upload fails;
        # Important response attributes:
        # 	UploadId   - identifier of the multipart upload

        create_multipart_upload_resp = await client.create_multipart_upload(
            ACL="bucket-owner-full-control",
            Bucket=AWS_S3_BUCKET_NAME,
            Key=key,
        )

        upload_id = create_multipart_upload_resp["UploadId"]

        tasks = []
        async with aiofiles.open(from_local_path, mode="rb") as file:
            for chunk_number in range(chunks_count):
                tasks.append(
                    upload_chunk(
                        client=client,
                        file=file,
                        chunk_number=chunk_number,
                        bytes_per_chunk=bytes_per_chunk,
                        key=key,
                        upload_id=upload_id,
                        source_size=source_size,
                    )
                )

            await asyncio.gather(*tasks)

        # Step 3 - list parts actually stored in s3
        # Important args:
        # 	Bucket     - bucket name where file will be stored;
        # 	UploadId   - id of the multipart upload which identifies uploading file;
        # 	Key        - path in S3 under which the file will be available;
        # Important response attributes:
        # 	Parts 	   - uploaded parts registered in S3;

        list_parts_resp = await client.list_parts(
            Bucket=AWS_S3_BUCKET_NAME, Key=key, UploadId=upload_id
        )

        # Step 4 - complete or abort multipart upload
        # Important args:
        # 	Bucket          - bucket name where file will be stored;
        # 	UploadId        - id of the multipart upload which identifies uploading file;
        # 	Key             - path in S3 under which the file will be available;
        #   MultipartUpload - dict with parts recorded info(part number and etag);
        # Important response attributes:
        # 	Location 	    - path where file is stored, might be used to save in db;

        # You have to sort parts in ascending order. Otherwise api will reject request
        part_list = sorted(part_info["Parts"], key=lambda k: k["PartNumber"])
        part_info["Parts"] = part_list
        print(part_info["Parts"][0])
        print("COMPLETED ", len(part_info["Parts"]))

        if len(list_parts_resp["Parts"]) == chunks_count:
            print("Done uploading file")
            await client.complete_multipart_upload(
                Bucket=AWS_S3_BUCKET_NAME,
                Key=key,
                UploadId=upload_id,
                MultipartUpload=part_info,
            )

            return True

        else:
            print("Aborted uploading file.")
            await client.abort_multipart_upload(
                Bucket=AWS_S3_BUCKET_NAME, Key=key, UploadId=upload_id
            )

            return False


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        begin_multipart_upload("./large.txt", to_s3_folder_path="large")
    )
