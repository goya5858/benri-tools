FROM pytorch/pytorch:latest

WORKDIR /app

COPY ./ .

# コンテナ内で必要なパッケージをインストール
RUN pip install -r requirements.txt 

EXPOSE 8000
# FastAPIを8000ポートで待機
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]