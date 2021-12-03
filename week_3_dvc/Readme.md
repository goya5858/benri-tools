DVCを用いてデータ/モデルのバージョン管理を行うデモです
このフォルダではモデルのバージョニングを行います

DVCではGitと併用してバージョン管理を行うといいです

1. DVCを初期化する

```
    >> dvc init
```
もし親ディレクトリでGit管理したい場合
```
    >> dvc init --subdir
```

2. DVCでデータ/モデル本体をPush(保存)するためのストレージorディレクトリを指定
```sh
    >> dvc remote add -d <任意のストレージ名> <path/to/remotestrage>
```
ex) Google Driveを使用する場合
```sh
    >> dvc remote add -d storage gdrive://1gf1vyFQPdgFOobjwTxcwSQ7JC1tATmku
```

3. モデル(ver.1.0.0)の作成
```
    >> python3 train.py
```
modelsフォルダに学習済みモデルが保存される

4. dvc addコマンドを実行する
```
    >> dvc add <path/to/model>
```
or   
  もう少しsmartな形式として、
```
    >> mkdir dvcfiles
    >> cd dvcfiles
    >> dvc add <path/to/model> --file <任意のモデル名>.dvc
```
としてdvcfilesにDVC関連のファイルをまとめる & モデルの名称をわかりやすくする  
ex) 
```
    >> mkdir dvcfiles
    >> cd dvcfiles
    >> dvc add ../models/best-checkpoint.ckpt --file trained_model.dvc
```

5. データ/モデルのpush
```
    >> dvc push --remote <送信したいサーバー名>
```
```
    >> dvc push --remote storage

    Enter verification code: VERYFICATION=CODE
    Authentication successful.
    1 file pushed         
```

6. Githubへ trained_model.dvcファイルのプッシュ  
    データ/モデル本体の代わりに"データ/モデル.dvcファイル"をGithubにアップロードして疑似的なバージョン管理を行う