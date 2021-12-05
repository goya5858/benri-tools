FROM public.ecr.aws/lambda/python:3.8

WORKDIR /app

COPY ./ .

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

# AWS credentials
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# コンテナ内で必要なパッケージをインストール
RUN pip install -r requirements.txt 
RUN pip install dvc[s3]

# DVC pulling model stored at remote-strage
RUN dvc init --no-scm
RUN dvc remote add -d model-store s3://models-dvc-goya/trained_model
RUN cat .dvc/config
RUN dvc pull dvcfiles/trained_model.dvc


EXPOSE 8000
# FastAPIを8000ポートで待機
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["main.handler"]