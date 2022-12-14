# NOTE: .envから環境変数を読み込もうとしたが、エラーとなった。
# Deployment ManagerのPythonテンプレートでは特定のパッケージ以外は特別な方法でインポートする必要があるみたい。
# import importlib.util as util
# import sys

# spec = util.spec_from_file_location("os", "/usr/local/lib/python3.10/os.py")
# os = util.module_from_spec(spec)
# sys.modules["os"] = os
# spec.loader.exec_module(os)

# dotenv_path = "/usr/local/lib/python3.10/site-packages/dotenv/__init__.py"
# spec = util.spec_from_file_location("dotenv", dotenv_path)
# dotenv = util.module_from_spec(spec)
# sys.modules["dotenv"] = dotenv
# spec.loader.exec_module(dotenv)


# load_dotenv(verbose=True)
# pj_root_path = Path(__file__).parent.parent
# dotenv_path = pj_root_path / ".env"
# load_dotenv(dotenv_path)


def GenerateConfig(context):
    """Generate configuration."""

    # General setting
    PROJECT_ID = context.env["project"]
    PROJECT_NUMBER = context.env["project_number"]
    ZONE = context.properties["zone"]

    # Service Account
    SERVICE_ACCOUNT_ID = context.properties["serviceAccountId"]
    SERVICE_ACCOUNT_DISPLAYNAME = context.properties["serviceAccountDisplayName"]
    SERVICE_ACCOUNT = f"{SERVICE_ACCOUNT_ID}@{PROJECT_ID}.iam.gserviceaccount.com"
    COMPUTE_SERVICE_ACCOUNT = f"{PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

    # Storage
    # BUCKET_NAME = os.environ.get("BUCKET_NAME")
    BUCKET_NAME = "bucket-" + context.env["project"]
    DATASET_NAME = context.properties["datasetName"]
    TABLE_NAME = context.properties["tableName"]

    resources = []

    # Enable Compute Engine API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-compute-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "compute.googleapis.com",
            },
        }
    )
    # Enable Cloud Storage API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-storage-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "storage.googleapis.com",
            },
        }
    )
    # Enable BigQuery Storage API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-bigquery-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "bigquery.googleapis.com",
            },
        }
    )
    # Enable Vertex AI API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-aiplatform-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "aiplatform.googleapis.com",
            },
        }
    )
    # Enable Identity and Access Management (IAM) API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-iam-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "iam.googleapis.com",
            },
        }
    )
    # Enable Cloud Resource Manager API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-cloud-resource-manager-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "cloudresourcemanager.googleapis.com",
            },
        }
    )
    # Enable Artifact Registry API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-artifact-registry-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "artifactregistry.googleapis.com",
            },
        }
    )
    # Enable Cloud Build API
    resources.append(
        {
            "type": "deploymentmanager.v2.virtual.enableService",
            "name": "enable-cloud-build-api",
            "properties": {
                "consumerId": f"project: {PROJECT_ID}",
                "serviceName": "cloudbuild.googleapis.com",
            },
        }
    )

    # Enable Creat a serivece account
    resources.append(
        {
            "type": "iam.v1.serviceAccount",
            "name": "app-service-account",
            "properties": {
                "accountId": SERVICE_ACCOUNT_ID,
                "displayName": SERVICE_ACCOUNT_DISPLAYNAME,
                "projectId": PROJECT_ID,
            },
            "metadata": {
                "dependsOn": ["enable-iam-api", "enable-cloud-resource-manager-api"]
            },
        }
    )

    # Add a role to the app serivece account
    resources.append(
        {
            "type": "gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding",
            "name": "bind-iam-policy-aiplatform.user",
            "properties": {
                "resource": PROJECT_ID,
                "role": "roles/aiplatform.user",
                # NOTE: "serviceAccount:value" 全体を文字列としないとエラーとなる
                "member": f"serviceAccount:{SERVICE_ACCOUNT}",
            },
            "metadata": {"dependsOn": ["app-service-account"]},
        }
    )
    resources.append(
        {
            "type": "gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding",
            "name": "bind-iam-policy-objectCreater",
            "properties": {
                "resource": PROJECT_ID,
                "role": "roles/storage.objectCreator",
                # NOTE: "serviceAccount:value" 全体を文字列としないとエラーとなる
                "member": f"serviceAccount:{SERVICE_ACCOUNT}",
            },
            "metadata": {"dependsOn": ["app-service-account"]},
        }
    )
    resources.append(
        {
            "type": "gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding",
            "name": "bind-iam-policy-objectViewer",
            "properties": {
                "resource": PROJECT_ID,
                "role": "roles/storage.objectViewer",
                # NOTE: "serviceAccount:value" 全体を文字列としないとエラーとなる
                "member": f"serviceAccount:{SERVICE_ACCOUNT}",
            },
            "metadata": {"dependsOn": ["app-service-account"]},
        }
    )
    resources.append(
        {
            "type": "gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding",
            "name": "bind-iam-policy-storage.admin",
            "properties": {
                "resource": PROJECT_ID,
                "role": "roles/storage.admin",
                # NOTE: "serviceAccount:value" 全体を文字列としないとエラーとなる
                "member": f"serviceAccount:{SERVICE_ACCOUNT}",
            },
            "metadata": {"dependsOn": ["app-service-account"]},
        }
    )
    resources.append(
        {
            "type": "gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding",
            "name": "bind-iam-policy-serviceAccountUser",
            "properties": {
                "resource": PROJECT_ID,
                "role": "roles/iam.serviceAccountUser",
                # NOTE: "serviceAccount:value" 全体を文字列としないとエラーとなる
                "member": f"serviceAccount:{SERVICE_ACCOUNT}",
            },
            "metadata": {"dependsOn": ["app-service-account"]},
        }
    )

    # Add roles to compute service accountis
    resources.append(
        {
            "type": "gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding",
            "name": "bind-iam-policy-objectCreater-compute",
            "properties": {
                "resource": PROJECT_ID,
                "role": "roles/storage.objectCreator",
                # NOTE: "serviceAccount:value" 全体を文字列としないとエラーとなる
                "member": f"serviceAccount:{COMPUTE_SERVICE_ACCOUNT}",
            },
            "metadata": {"dependsOn": ["app-service-account"]},
        }
    )
    resources.append(
        {
            "type": "gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding",
            "name": "bind-iam-policy-objectViewer-compute",
            "properties": {
                "resource": PROJECT_ID,
                "role": "roles/storage.objectViewer",
                # NOTE: "serviceAccount:value" 全体を文字列としないとエラーとなる
                "member": f"serviceAccount:{COMPUTE_SERVICE_ACCOUNT}",
            },
            "metadata": {"dependsOn": ["app-service-account"]},
        }
    )

    # Create a storage bucket
    resources.append(
        {
            "type": "storage.v1.bucket",
            "name": BUCKET_NAME,  # Deployment name and bucket name
            "properties": {
                "resource": PROJECT_ID,
                "location": ZONE,
                "predefinedAcl": "projectPrivate",
                "projection": "full",
                "storageClass": "STANDARD",
            },
        }
    )

    # Create a dataset on BigQuery
    resources.append(
        {
            "type": "bigquery.v2.dataset",
            "name": "demo_dataset",
            "properties": {
                "datasetReference": {
                    "datasetId": DATASET_NAME,  # Actual dataset name
                },
                "location": ZONE,
                "description": "dataset for kubeflow demo",
            },
        }
    )
    # Create a table on BigQuery
    resources.append(
        {
            "type": "bigquery.v2.table",
            "name": "demo_table",
            "properties": {
                "datasetId": DATASET_NAME,  # Actual dataset name
                "tableReference": {
                    "tableId": TABLE_NAME,  # Actual dataset name
                },
            },
            "metadata": {"dependsOn": ["enable-bigquery-api", "demo_dataset"]},
        }
    )

    return {"resources": resources}
