Hydraを実践するためのサンプルです

Hydraは実行コードに
    @hydra.main(~~~~)
    def main(cfg):
        ~~~
        ~~~
のように変更するのみで実装可能です

1. train.ipynbはモデルを学習するノートブックです
   Hydraはコマンドラインで実行するため、このノートブックをPythonファイルに変換します
   >> jupyter nbconvert train.ipynb --to python

2. Hydraは以下のコマンドで実行可能です
    >> python3 train.py model.hidden_size=24

3. MLFlowで結果を確認する
    まずは mlrunsのあるディレクトリに移動
    >> cd outputs/2021-12-03/09-46-26 
    >> mlflow ui --port 5000