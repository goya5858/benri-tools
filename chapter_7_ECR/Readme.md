GithubActionsを用いたCIテスト

chapter5でコンテナでパッケージ化したモデルのアップデートをする際、テストをGitHubへのPushと同時に自動的に行う -> CI

ディレクトリの中身はChap.5とほぼ同じ(model本体が含まれる+sample.ipynbは除外)

1. .gitフォルダが存在する親ディレクトリに
    ```
    .github/workflows
    ```
   ディレクトリを作成  
この中にCI用の設定ファイルを作成する

2. Workファイルの作成  
Dockerコンテナを自動デプロイするジョブを設定する
```yaml
name: Create Docker Container

on: [push]

jobs: 
  mlops-container:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./chapter_6_GithubActions
    steps:
      - name: Checkout
        uses: actions/checkout@v2
        with:
          ref: ${{ github.ref }}
      
      - name: Build container
        run: |
          docker network create data
          docker compose up --build
```

3. GitHibのＨＰにアクセスし、Actionsを開いて適当に設定する(ほぼデフォルトでOK)  
GithubではデフォルトでActionsがONになっているので、基本的に2. のファイルを設置してPUSHするのみでOK
