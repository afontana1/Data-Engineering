import boto3
import datetime

try:
    from .config import boto3_config
except ImportError as e:
    boto3_config = {}


class LamdaMetrics:
    def __init__(self, starttime: datetime, endtime: datetime, target: str = ""):
        if starttime >= endtime:
            raise Exception(
                f"starttime {str(starttime)} needs to be less than endtime {str(endtime)}"
            )

        self.client = boto3.client("cloudwatch", **boto3_config)
        self.target = target
        self.metric_stats = {
            "Namespace": "AWS/Lambda",
            "StartTime": starttime,
            "EndTime": endtime,
            "Period": 60,
            "Dimensions": [
                {"Name": "FunctionName", "Value": self.target},
            ],
        }

    def __str__(self):
        return f"Metrics for {self.target}"

    @property
    def duration(self):
        return {
            "MetricName": "Duration",
            "Statistics": ["Average"],
            "Unit": "Milliseconds",
        }

    @property
    def invocations(self):
        return {"MetricName": "Invocations", "Statistics": ["Sum"], "Unit": "Count"}

    @property
    def errors(self):
        return {"MetricName": "errors", "Statistics": ["Sum"], "Unit": "Count"}

    def _set_metric_stats(self, metric: str):
        if metric not in self.__dir__():
            raise Exception(f"{metric} Not a defined metric.")
        self.metric_stats.update(getattr(self, metric))

    def get_metric_statistics(self, metric: str):
        self._set_metric_stats(metric)
        return self.client.get_metric_statistics(**self.metric_stats)
