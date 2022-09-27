### GCP ###
load-env:
	. ./.env

setup-gcloud-cli:
	bash .gcp/setup_gcloud.sh
# This command should be run as a project owner
# (run "gcloud auth login" to be an owner account) 
deploy-resources-jinja:
	gcloud deployment-manager deployments \
		create kubeflow-demo-deployment --config .gcp/jinja-template/deployment-jinja.yml

delete-resources-jinja:
	gcloud deployment-manager deployments \
		delete kubeflow-demo-deployment --delete-policy=DELETE


deploy-resources-python:
	gcloud deployment-manager deployments \
		create kubeflow-demo-deployment --config .gcp/python-template/deployment-py.yml

delete-resources-python:
	gcloud deployment-manager deployments \
		delete kubeflow-demo-deployment --delete-policy=DELETE

enable-services:
	gcloud services enable \
		iam.googleapis.com \
		cloudresourcemanager.googleapis.com \
		aiplatform.googleapis.com

# computeやstorageは停止しないでおく。
disable-services:
	gcloud services disable \
		iam.googleapis.com \
		cloudresourcemanager.googleapis.com \
		aiplatform.googleapis.com