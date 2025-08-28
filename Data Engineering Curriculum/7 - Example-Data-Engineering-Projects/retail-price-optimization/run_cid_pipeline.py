import click

from constants import MODEL_NAME, PIPELINE_NAME, PIPELINE_STEP_NAME
from pipelines.inference_pipeline import inference_fashion_mnist

# from pipelines.inference_pipeline impor
from pipelines.training_pipeline import training_retail

DEPLOY = "deploy"
PREDICT = "predict"
DEPLOY_AND_PREDICT = "deploy_and_predict"


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Choice([DEPLOY, PREDICT, DEPLOY_AND_PREDICT]),
    default="deploy_and_predict",
    help="Optionally you can choose to only run the deployment "
    "pipeline to train and deploy a model (`deploy`), or to "
    "only run a prediction against the deployed model "
    "(`predict`). By default both will be run "
    "(`deploy_and_predict`).",
)
def main(
    config: str,
):
    deploy = config == DEPLOY or config == DEPLOY_AND_PREDICT
    predict = config == PREDICT or config == DEPLOY_AND_PREDICT

    if deploy:
        training_retail()
        # data_drift_step = last_run.get_step(step="deepchecks_model_drift_check_step")
        # model_drift_step = last_run.get_step(step="deepchecks_model_validation_check_step")

    if predict:
        inference_fashion_mnist(
            model_name=MODEL_NAME,
            pipeline_name=PIPELINE_NAME,
            step_name=PIPELINE_STEP_NAME,
        )


if __name__ == "__main__":
    main()
