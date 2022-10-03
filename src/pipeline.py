import kfp

from config import (
    DATASET_DISPLAY_NAME,
    ENDPOINT_DISPLAY_NAME,
    GCS_CSV_PATH,
    MODEL_DEPLOY_MACHINE_TYPE,
    MODEL_DEPLOY_MAX_REPLICA_COUNT,
    MODEL_DEPLOY_MIN_REPLICA_COUNT,
    PROJECT_ID,
    REGION,
    TRAINING_BUDGET_MILLI_NODE_HOURS,
    TRAINING_DISPLAY_NAME,
    TRAINING_OPTIMIZATION_OBJECTIVE,
    TRAINING_PREDICTION_TYPE,
)


@kfp.dsl.pipeline(name="automl-tab-training-v2")
def pipeline():
    """Define a ML pipeline."""
    from google_cloud_pipeline_components import aiplatform as gcc_aip
    from google_cloud_pipeline_components.v1.endpoint import (
        EndpointCreateOp,
        ModelDeployOp,
    )

    dataset_create_op = gcc_aip.TabularDatasetCreateOp(
        project=PROJECT_ID,
        location=REGION,
        display_name=DATASET_DISPLAY_NAME,
        gcs_source=GCS_CSV_PATH,
    )

    training_op = gcc_aip.AutoMLTabularTrainingJobRunOp(
        project=PROJECT_ID,
        location=REGION,
        display_name=TRAINING_DISPLAY_NAME,
        optimization_prediction_type=TRAINING_PREDICTION_TYPE,
        optimization_objective=TRAINING_OPTIMIZATION_OBJECTIVE,
        budget_milli_node_hours=TRAINING_BUDGET_MILLI_NODE_HOURS,
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
        project=PROJECT_ID,
        location=REGION,
        display_name=ENDPOINT_DISPLAY_NAME,
    )

    _ = ModelDeployOp(
        model=training_op.outputs["model"],
        endpoint=endpoint_op.outputs["endpoint"],
        dedicated_resources_machine_type=MODEL_DEPLOY_MACHINE_TYPE,
        dedicated_resources_min_replica_count=MODEL_DEPLOY_MIN_REPLICA_COUNT,
        dedicated_resources_max_replica_count=MODEL_DEPLOY_MAX_REPLICA_COUNT,
    )
