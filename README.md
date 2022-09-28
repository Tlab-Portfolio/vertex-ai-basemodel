# mlops_template

## Setup
1. Login to the Google Cloud console
2. Create a new project
3. Copy the project ID and paste it on `.env` file
4. Run the folllowing command on a local bash
```
# Prepare to run deployment manger
make setup-gcloud-cli

# Run deployment manager
make deploy-resources-python
```


### Vertex AI Pipeline code comes from this Notebook
https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/pipelines/google_cloud_pipeline_components_automl_tabular.ipynb