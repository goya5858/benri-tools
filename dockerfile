FROM pytorch/pytorch:1.8.1-cuda10.2-cudnn7-runtime

RUN pip3 install --upgrade pip && \
    pip3 install \ 
    pandas       matplotlib        seaborn \
    sklearn      lightgbm \
    torchmetrics pytorch-lightning \
    timm         transformers\
    mlflow       optuna \
    hydra-core 　omegaconf \
    onnx \
    jupyter \
    torchvision  albumentations \
    slugify && \
    pip3 install --upgrade --force-reinstall --no-deps kaggle && \
    pip3 install -U ipykernel --user
    
RUN apt update -y && \
    apt install git -y && \
    apt install -y curl jq git-secret && \
    apt-get install unzip

RUN conda install -c rapidsai -c nvidia -c numba -c conda-forge cudf=21.06 python=3.7 cudatoolkit=11.0
RUN conda install -c rapidsai -c nvidia -c numba -c conda-forge cuml=21.06 -y
RUN pip3 uninstall -y pandas && \
    pip3 install pandas==1.3.0

COPY ./subfiles/.kaggle/ /root/.kaggle
COPY ./subfiles/.ssh /root/.ssh

COPY ./subfiles/git-script-for-docker.sh /root
ENTRYPOINT ["sh", "/root/git-script-for-docker.sh"]