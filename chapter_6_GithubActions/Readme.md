FastAPIを用いた簡単なアプリの実装  
1. テスト
```
    >> uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```  

コマンドを実行すると、現在作業中のコンテナの外にて、  
```
    localhost:8000/  
        へのアクセスでトップページ
    localhost:8000/docs
        へのアクセスで Swagger形式のDocへアクセス、実装したコマンドのテストができる
```

2. アプリの実装  
    作業用コンテナの外からこのディレクトリに移動し、新たにアプリデプロイ用のコンテナを起動する
    ```
    >> docker compose up
     or
    >> docker compose up --build
    ```
3. localhost:8000/docsへのアクセスでアプリへアクセスできる