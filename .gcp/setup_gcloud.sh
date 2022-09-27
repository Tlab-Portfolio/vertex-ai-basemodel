#! /usr/bin/env bash

# 環境変数を読み込む
source .env

# ローカルにおけるgcloudコマンドの設定
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION

# Deployment Manger APIを有効にする
gcloud services enable deploymentmanager.googleapis.com

# 機密情報を使ったサービスアカウントの有効化
# gcloud auth activate-service-account --key-file .gcp/GCP_credential.json
