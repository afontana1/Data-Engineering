import paramiko
import boto3
from io import BytesIO
from stat import S_ISDIR, S_ISREG

from boto3.s3.transfer import TransferConfig

# Set the desired multipart threshold value (1GB)
GB = 1024**3
config = TransferConfig(multipart_threshold=1 * GB)

password = "the_sftp_password"
username = "the_sftp_username"

# depending on how this code is to be run you may need to set up a
# boto3 session first, called with your AWS profile name
# before calling the boto3.resource line, like this:-
#
# AWS_PROFILE='my-profile'
# session = boto3.Session(profile_name=AWS_PROFILE)
# s3 = session.resource('s3')


def lambda_handler(event, context=None):
    """Transfer from SFTP to S3"""
    s3 = boto3.resource("s3")
    s3client = boto3.client("s3")

    host = "your_sftp_address"
    port = "your_sftp_portnumber"
    # Create a Transport object
    transport = paramiko.Transport((host, port))
    # Connect to a Transport server
    transport.connect(username=username, password=password)
    # Create an SFTP client
    with paramiko.SFTPClient.from_transport(transport) as sftp:
        # change to a subdirectory if required
        sftp.chdir("/my-sub-folder")
        for entry in sftp.listdir_attr(""):
            mode = entry.st_mode
            # we have a regular file, not a folder
            if S_ISREG(mode):

                f = entry.filename
                with BytesIO() as data:
                    print("Downloading file {0} from SFTP.. to S3".format(f))
                    sftp.getfo(f, data)
                    data.seek(0)
                    s3client.upload_fileobj(
                        data,
                        "your_s3_bucket_name",
                        "your_s3_folder_name/{0}".format(f),
                        Config=config,
                    )
