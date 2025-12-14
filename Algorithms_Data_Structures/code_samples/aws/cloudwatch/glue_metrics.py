import boto3
import functools
import logging
from botocore.exceptions import ClientError

try:
    from .config import boto3_config
except ImportError as e:
    boto3_config = {}

logger = logging.getLogger(__name__)


class GlueMetrics:
    """Encapsulates AWS Glue actions."""

    def __init__(self):
        """
        :param glue_client: A Boto3 Glue client.
        """
        self.glue_client = boto3.client("glue", **boto3_config)

    def _unpack(self, func, target_data, *args, **kwargs):
        results = []
        continuation_token = None
        try:
            while True:
                list_kwargs = {}
                list_kwargs.update(**kwargs)
                if continuation_token:
                    list_kwargs["NextToken"] = continuation_token
                response = func(**list_kwargs)
                results += response.get(f"{target_data}", [])
                continuation_token = response.get("NextToken")
                if not continuation_token:
                    break
        except ClientError as err:
            logger.error(
                f"Couldn't {str(func).split('.')[-1]}. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}",
            )
            raise
        else:
            return results

    @functools.lru_cache
    def list_jobs(self):
        """
        Lists the names of job definitions in your account.

        :return: The list of job definition names.
        """
        return getattr(self, "_unpack")(self.glue_client.list_jobs, "JobNames")

    def get_job_runs(self, job_name, most_recent=False):
        """
        Gets information about runs that have been performed for a specific job
        definition.

        :param job_name: The name of the job definition to look up.
        :return: The list of job runs.
        """
        return (
            self.glue_client.get_job_runs(JobName=job_name).get("JobRuns")
            if most_recent
            else getattr(self, "_unpack")(
                self.glue_client.get_job_runs, "JobRuns", JobName=job_name
            )
        )

    @functools.lru_cache
    def get_job_run(self, job_name, run_id):
        """
        Gets information about a single job run.

        :param name: The name of the job definition for the run.
        :param run_id: The ID of the run.
        :return: Information about the run.
        """
        try:
            response = self.glue_client.get_job_run(
                JobName=job_name, RunId=run_id, PredecessorsIncluded=True | False
            )
        except ClientError as err:
            logger.error(
                "Couldn't get job run %s/%s. Here's why: %s: %s",
                job_name,
                run_id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response
