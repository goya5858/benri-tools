#!/bin/sh
git config --global user.name $(cat ~/.ssh/env.json | jq ".user.username")
git config --global user.email $(cat ~/.ssh/env.json | jq ".user.useremail")

# コンテナを起動し続ける
tail -f /dev/null