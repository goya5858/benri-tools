FROM pytorch/pytorch:latest

#RUN conda install -c rapidsai -c nvidia -c numba -c conda-forge cudf=21.08 python=3.7 cudatoolkit=11.2
#RUN conda install -c rapidsai -c nvidia -c numba -c conda-forge cuml=21.08 -y

RUN apt update -y && \
    apt install git -y && \
    apt install wget -y && \
    apt install -y curl jq git-secret && \
    apt-get install unzip

#RUN pip uninstall torch -y && \
#RUN pip uninstall torchtext -y

RUN pip3 install --upgrade pip && \
    pip3 install \ 
    matplotlib   seaborn    pandas==1.3.0 \
    sklearn      lightgbm \
    #torch==1.10.0 \
    #torchtext==0.11.0 \
    pytorch-lightning==1.4.9 \
    torchmetrics>=0.3 \
    timm         transformers\
    mlflow       optuna \
    hydra-core 　omegaconf \
    dvc dvc[gdrive] dvc[ssh] \
    onnx \
    jupyter \
    albumentations \
    slugify && \
    pip3 install --upgrade --force-reinstall --no-deps kaggle && \
    pip3 install -U ipykernel --user

COPY ./subfiles/.kaggle/ /root/.kaggle
COPY ./subfiles/.ssh /root/.ssh

COPY ./subfiles/git-script-for-docker.sh /root
ENTRYPOINT ["sh", "/root/git-script-for-docker.sh"]