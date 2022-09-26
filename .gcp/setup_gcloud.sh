#! /usr/bin/env bash

# 環境変数を読み込む
source .env

# gcloudコマンドの設定
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION

# 機密情報を使ったサービスアカウントの有効化
# gcloud auth activate-service-account --key-file .gcp/GCP_credential.json
