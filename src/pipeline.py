import google.cloud.aiplatform as aip
import kfp

from config import BUCKET_URI, GCS_CSV_PATH, PROJECT_ID, REGION


@kfp.dsl.pipeline(name="automl-tab-training-v2")
def pipeline(project: str = PROJECT_ID, region: str = REGION):
    from google_cloud_pipeline_components import aiplatform as gcc_aip
    from google_cloud_pipeline_components.v1.endpoint import (
        EndpointCreateOp,
        ModelDeployOp,
    )

    dataset_create_op = gcc_aip.TabularDatasetCreateOp(
        project=project,
        location=region,
        display_name="housing",
        gcs_source=GCS_CSV_PATH,
    )

    training_op = gcc_aip.AutoMLTabularTrainingJobRunOp(
        project=project,
        location=region,
        display_name="train-automl-cal_housing",
        optimization_prediction_type="regression",
        optimization_objective="minimize-rmse",
        column_transformations=[
            {"numeric": {"column_name": "longitude"}},
            {"numeric": {"column_name": "latitude"}},
            {"numeric": {"column_name": "housing_median_age"}},
            {"numeric": {"column_name": "total_rooms"}},
            {"numeric": {"column_name": "total_bedrooms"}},
            {"numeric": {"column_name": "population"}},
            {"numeric": {"column_name": "households"}},
            {"numeric": {"column_name": "median_income"}},
            {"numeric": {"column_name": "median_house_value"}},
        ],
        dataset=dataset_create_op.outputs["dataset"],
        target_column="median_house_value",
    )

    endpoint_op = EndpointCreateOp(
        project=project,
        location=region,
        display_name="train-automl-cal_housing_endpoint",
    )

    _ = ModelDeployOp(
        model=training_op.outputs["model"],
        endpoint=endpoint_op.outputs["endpoint"],
        dedicated_resources_machine_type="n1-standard-4",
        dedicated_resources_min_replica_count=1,
        dedicated_resources_max_replica_count=1,
    )
