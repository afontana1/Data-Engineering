from datetime import datetime
from typing import Union
import json
from dataclasses import dataclass, asdict, is_dataclass


class EnhancedJSONEncoder(json.JSONEncoder):
    """Usage: json.dumps(foo, cls=EnhancedJSONEncoder)
    https://www.bruceeckel.com/2018/09/16/json-encoding-python-dataclasses/
    """

    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


@dataclass
class Base:
    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class LambdaRecord(Base):
    metric_name: str
    job_name: str
    timestamp: datetime
    statistic: Union[float, int]
    unit: str

    def __post_init__(self):
        """Validate types and convert datetime"""
        for x in [self.metric_name, self.job_name, self.unit]:
            if not isinstance(x, str):
                raise ValueError(f"{x} is of wrong type, must be string")

        if not isinstance(self.timestamp, datetime):
            raise ValueError(f"{self.timestamp} needs to be a datetime object")

        if not isinstance(self.statistic, (int, float)):
            raise ValueError(
                f"Wrong type for statistic,{self.statistic}. Needs to be float or int"
            )

        self.timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")


@dataclass
class GlueRecord(Base):
    JobName: str
    StartedOn: datetime
    LastModifiedOn: datetime
    CompletedOn: datetime
    JobRunState: str
    ExecutionTime: str

    def __post_init__(self):
        """Validate types and convert datetime"""
        for field_name, date_obj in [
            ("StartedOn", self.StartedOn),
            ("LastModifiedOn", self.LastModifiedOn),
            ("CompletedOn", self.CompletedOn),
        ]:
            if not isinstance(date_obj, datetime):
                raise ValueError(f"{date_obj} is of wrong type, must be datetime")

            setattr(self, field_name, date_obj.strftime("%Y-%m-%d %H:%M:%S.%f"))

        for x in [self.JobName, self.JobRunState, self.ExecutionTime]:
            if not isinstance(x, (str, int, float)):
                raise ValueError(f"{x} is of wrong type, must be string,int,or float")


class LambdaParser:
    """Parse results from Glue and Lambda API"""

    def __init__(self, job_name):
        self.job_name = job_name

    def parse_lambda_metrics(self, records):
        """Flatten records"""
        results = []
        metric_name = records.get("Label", "")
        data_points = records.get("Datapoints", "")
        if (not metric_name) or (not data_points):
            return results
        for record in data_points:
            results.append(
                LambdaRecord(
                    metric_name=metric_name,
                    job_name=self.job_name,
                    timestamp=record.get("Timestamp"),
                    statistic=record.get("Sum") or record.get("Average"),
                    unit=f"{'Sum' if record.get('Sum') else 'Average'}|{record.get('Unit')}",
                )
            )
        return results


class GlueParser:
    def __init__(self, name):
        self.name = name

    def parse_single_record(self, record):
        return GlueRecord(
            JobName=record.get("JobName"),
            StartedOn=record.get("StartedOn"),
            LastModifiedOn=record.get("LastModifiedOn"),
            CompletedOn=record.get("CompletedOn"),
            JobRunState=record.get("JobRunState"),
            ExecutionTime=record.get("ExecutionTime"),
        )

    def parse_glue_metrics(self, records):
        results = []
        for record in records:
            results.append(self.parse_single_record(record))
        return results
