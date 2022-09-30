# mlops_template

## Setup
1. Login to the Google Cloud console
2. Create a new project
3. Copy the project ID and paste it on `.env` file
4. Check values on configuration files 
    - `.env`
    - If use python template for Deployment Manager
        - `.gcp/python-template/deployment-py.yml`
    - If use jinja template for Deployment Manager
        - `.gcp/jinja-template/deployment-jinja.yml`
5. Run the folllowing command on a local bash
```
# Prepare to run deployment manger
make setup-gcloud-cli

# Run deployment manager
make deploy-resources-python

```
6. Create a service account key json file on GCP Console and store it to the following path
`.gcp/gcp_serice_account_key.json`

7. Run python scripts
```
make compile-and-run

```
### Vertex AI Pipeline code comes from this Notebook
https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/pipelines/google_cloud_pipeline_components_automl_tabular.ipynb