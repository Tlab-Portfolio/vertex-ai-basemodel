# 環境変数を読み込む
load-env:
	. ./.env

# Deployment Managerを利用する準備を行う
setup-gcloud-cli:
	bash .gcp/setup_gcloud.sh


### Deployment Managerを使ってGCPのリソースを管理する ##
#   (This command should be run as a project owner. run "gcloud auth login" to be an owner account) 

# jinjaのテンプレートを使う場合
deploy-resources-jinja:
	gcloud deployment-manager deployments \
		create kubeflow-demo-deployment --config .gcp/jinja-template/deployment-jinja.yml

delete-resources-jinja:
	gcloud deployment-manager deployments \
		delete kubeflow-demo-deployment --delete-policy=DELETE

# pythonのテンプレートを使う場合
deploy-resources-python:
	gcloud deployment-manager deployments \
		create kubeflow-demo-deployment --config .gcp/python-template/deployment-py.yml

delete-resources-python:
	gcloud deployment-manager deployments \
		delete kubeflow-demo-deployment --delete-policy=DELETE


# GCPのサービスを有効化する
# (プロジェクト作成時から有効化されているAPI 及び Compute Engine APIは含めない。) 
enable-services:
	gcloud services enable \
		iam.googleapis.com \
		cloudresourcemanager.googleapis.com \
		aiplatform.googleapis.com \
		artifactregistry.googleapis.com \
		cloudbuild.googleapis.com

# GCPのサービスを無効化する
# (プロジェクト作成時から有効化されているAPI 及び Compute Engine APIは含めない。)
disable-services:
	gcloud services disable \
		iam.googleapis.com \
		cloudresourcemanager.googleapis.com \
		aiplatform.googleapis.com \
		artifactregistry.googleapis.com \
		cloudbuild.googleapis.com
