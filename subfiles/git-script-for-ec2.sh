#!/bin/sh
sudo cp /home/ubuntu/kaggle-template/subfiles/.ssh/config ~/.ssh/
sudo cp /home/ubuntu/kaggle-template/subfiles/.ssh/env.json ~/.ssh/
sudo cp /home/ubuntu/kaggle-template/subfiles/.ssh/id_rsa.GitHub_goya5858 ~/.ssh/
sudo cp /home/ubuntu/kaggle-template/subfiles/.kaggle/kaggle.json ~/.kaggle/

sudo pip3 install slugify
sudo pip3 install --upgrade --force-reinstall --no-deps kaggle

sudo apt -y update
sudo apt -y install jq git-secret
git config --global user.name $(cat ~/.ssh/env.json | jq ".user.username")
git config --global user.email $(cat ~/.ssh/env.json | jq ".user.useremail")