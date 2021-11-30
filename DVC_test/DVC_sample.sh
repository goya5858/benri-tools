#!/bin/sh

cd "任意のディレクトリに移動"
git init
dvc init

# GitHubのリモートサーバーにpush
git add .
git commit -m "make DVC"
git remote add origin "GithubのリポジトリURL"
git push -u origin main

# DVCのデータの実態を保存する Local/Remote サーバーを設定
dvc remote add -d "任意のサーバー名" path/to/server

# DVCを使って、データをpush
dvc add path/to/data
dvc push --remote "送信したいサーバー名"

# DVCを使って保存したデータをpull
dvc pull --remote "受信したいサーバー名"