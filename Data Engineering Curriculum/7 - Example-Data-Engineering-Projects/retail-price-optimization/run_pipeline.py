# from pipelines.training_pipeline import training_pipeline
from zenml import pipeline
from zenml.logger import get_logger

logger = get_logger(__name__)

from pipelines.training_pipeline import training_pipeline
from steps.ingest_data import ingest
from steps.process_data import categorical_encode

if __name__ == "__main__":
    training_pipeline()
