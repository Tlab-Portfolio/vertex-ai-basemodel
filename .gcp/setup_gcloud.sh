#! /usr/bin/env bash

# このスクリプトでは以下のタスクを行う
#  - ローカル環境におけるgcloudの設定
#  - Deployment Managerを使うために必要な設定

# 環境変数を読み込む
source .env

# ローカルにおけるgcloudコマンドの設定
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION

# Deployment Manger APIを有効にする
gcloud services enable deploymentmanager.googleapis.com

# Deployment Manager が利用するデフォルトのサービスアカウントにプロジェクトIAM管理者の権限を付与する
PROJECT_NUMBER=$(gcloud projects list \
                --filter="$(gcloud config get-value project)" \
                --format="value(PROJECT_NUMBER)")

DEFAULT_SERVICE_ACCOUNT="${PROJECT_NUMBER}@cloudservices.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${DEFAULT_SERVICE_ACCOUNT}" \
    --role="roles/resourcemanager.projectIamAdmin"

# 機密情報を使ったサービスアカウントの有効化
# gcloud auth activate-service-account --key-file .gcp/GCP_credential.json
