### GCP ###
load-env:
	. ./.env

setup-gcloud-cli:
	bash .gcp/setup_gcloud.sh
# This command should be run as a project owner
# (run "gcloud auth login" to be an owner account) 
deploy-resources:
	gcloud deployment-manager deployments \
	create kubeflow-demo-deployment --config .gcp/deployment.yml

delete-resources:
	gcloud deployment-manager deployments \
	delete kubeflow-demo-deployment --delete-policy=DELETE


deploy-resources-test:
	gcloud deployment-manager deployments \
	create kubeflow-demo-deployment --config .gcp/bucket.yml

delete-resources-test:
	gcloud deployment-manager deployments \
	delete kubeflow-demo-deployment --delete-policy=DELETE
	