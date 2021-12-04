FROM pytorch/pytorch:latest

RUN apt update -y && \
    apt install git -y && \
    apt install wget -y && \
    apt install -y curl jq git-secret && \
    apt-get install unzip

RUN pip3 install --upgrade pip && \
    pip3 install \ 
    matplotlib   seaborn    pandas==1.3.0 \
    sklearn      \
    pytorch-lightning==1.4.9 \
    torchmetrics>=0.3 \
    mlflow       optuna \
    hydra-core 　omegaconf \
    boto3 \
    dvc dvc[gdrive] dvc[ssh] dvc[s3]\
    onnx onnxruntime \
    fastapi uvicorn \
    jupyter \
    albumentations \
    slugify && \
    pip3 install --upgrade --force-reinstall --no-deps kaggle && \
    pip3 install -U ipykernel --user

COPY ./subfiles/.kaggle/ /root/.kaggle
COPY ./subfiles/.ssh /root/.ssh

COPY ./subfiles/git-script-for-docker.sh /root
ENTRYPOINT ["sh", "/root/git-script-for-docker.sh"]