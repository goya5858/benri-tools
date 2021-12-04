#!/bin/sh
git config --global user.name $(cat ~/.ssh/env.json | jq ".user.username")
git config --global user.email $(cat ~/.ssh/env.json | jq ".user.useremail")

# ssh-keyのpermissionを変更する
chmod 400 /root/.ssh/github_ssh

# Gitのデフォルトブランチを main に変更
git config --global init.defaultBranch main

# AWS CLI用のクレデンシャル情報をコンテナの環境変数に設定
AWS_ACCESS_KEY_ID=$(cat ~/.ssh/env.json | jq ".secrets.AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID=$(cat ~/.ssh/env.json | jq ".secrets.AWS_SECRET_ACCESS_KEY_ID")

# コンテナを起動し続ける
tail -f /dev/null