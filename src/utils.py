from pprint import pprint
from typing import Dict

from google.cloud import aiplatform, aiplatform_v1

from config import API_ENDPOINT, PROJECT_ID, REGION, TRAINING_DISPLAY_NAME


def delete_endpoint(
    endpoint_id: str,
    api_endpoint: str = API_ENDPOINT,
    project: str = PROJECT_ID,
    location: str = REGION,
    timeout: int = 300,
):
    """Delete an Endpoint on Vertex AI."""
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}

    # Initialize client.
    client = aiplatform.gapic.EndpointServiceClient(client_options=client_options)
    name = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.delete_endpoint(name=name)
    print("Long running operation:", response.operation.name)
    delete_endpoint_response = response.result(timeout=timeout)
    print("delete_endpoint_response:", delete_endpoint_response)


def delete_model(
    model_id: str,
    api_endpoint: str = API_ENDPOINT,
    project: str = PROJECT_ID,
    location: str = REGION,
    timeout: int = 300,
):
    """Delete a model on Vertex AI."""
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}

    # Initialize client.
    client = aiplatform.gapic.ModelServiceClient(client_options=client_options)
    name = client.model_path(project=project, location=location, model=model_id)
    response = client.delete_model(name=name)
    print("Long running operation:", response.operation.name)
    delete_model_response = response.result(timeout=timeout)
    print("delete_model_response:", delete_model_response)


def get_model_info(
    api_endpoint: str = API_ENDPOINT,
    project: str = PROJECT_ID,
    location: str = REGION,
    timeout: int = 300,
    model_display_name: str = None,
) -> Dict[str, str]:
    """Get information of trained model(s) on Vertex AI.

    Args:
        api_endpint (str): Vertex AI Endpoint API.
        project (str): Project ID on GCP.
        location (str): Region where Vertex AI models deployed.
        timeout (int): timeout after sending request to APIs.
        model_display_name (str): model display name to retlieve.

    Returns:
        results (Dict[str, str]): information about models deployed on
            Vertex AI.

    """
    # Initialize client.
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.ModelServiceClient(client_options=client_options)

    # Initialize request argument(s)
    parent = f"projects/{project}/locations/{location}"
    request = aiplatform_v1.ListModelsRequest(
        parent=parent,
    )

    # Make the request
    page_result = client.list_models(request=request, timeout=timeout)

    # Handle the response
    results = list()
    for model in page_result:
        model_info = {
            "model.name": model.name,
            "display_name": model.display_name,
            "version_id": model.version_id,
        }
        if len(model.deployed_models) != 0:
            model_info["deployed_endpoint"] = model.deployed_models[0].endpoint
            model_info["deployed_model_id"] = model.deployed_models[0].deployed_model_id
        results.append(model_info)

    # Filter infomation by model display name
    if model_display_name:
        results = [
            info for info in results if info["display_name"] == model_display_name
        ]
    return results


def undeploy_model_in_endpoint(
    endpoint_id: str,
    api_endpoint: str = API_ENDPOINT,
    project: str = PROJECT_ID,
    location: str = REGION,
    timeout: int = 300,
):
    """Undeploy a model in an endpoint of Vertex AI."""
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client
    client = aiplatform.gapic.EndpointServiceClient(client_options=client_options)

    model_info = get_model_info()

    for info in model_info:
        if (
            "deployed_endpoint" in info.keys()
            and endpoint_id in info["deployed_endpoint"]
        ):
            deployed_model_id = info["deployed_model_id"]

    endpoint_name = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    undeploy_request = aiplatform.gapic.UndeployModelRequest(
        endpoint=endpoint_name, deployed_model_id=deployed_model_id
    )
    client.undeploy_model(request=undeploy_request, timeout=timeout)


# get_model_info(model_display_name=TRAINING_DISPLAY_NAME)
# endpoint_id = "1124598085075337216"
# undeploy_model_in_endpoint(endpoint_id)
