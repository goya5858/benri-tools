Hydraを実践するためのサンプルです

Hydraは実行コードに
```
    @hydra.main(~~~~)
    def main(cfg):
        ~~~
        ~~~
```
のように変更するのみで実装可能です  

1. 元々のコードをHydraように変更
    ```python
    params = OmegaConf.load("configs/config.yaml")

    def main():
        model  = PLIrisModel(cfg=params)
        data   = PLIrisData()

        trainer = Trainer(
            gpus=1,
            max_epochs=30,
            callbacks=[ checkpoint_callback, early_stopping_callback ],
        )
        trainer.fit(model, data)

        ### MLFlow ###
        model.writer.set_terminated() # 必ず呼び出す！！
    ```
    ↓

    ```python
    @hydra.main(config_path="./configs", config_name="config")
    def main(cfg):
        model  = PLIrisModel(cfg=cfg)
        data   = PLIrisData()

        trainer = Trainer(
            gpus=1,
            max_epochs=30,
            callbacks=[ checkpoint_callback, early_stopping_callback ],
        )
        trainer.fit(model, data)

        ### MLFlow ###
        model.writer.set_terminated() # 必ず呼び出す！！
    ```

2. train.ipynbはモデルを学習するノートブックです
   Hydraはコマンドラインで実行するため、このノートブックをPythonファイルに変換します
   ```sh
   >> jupyter nbconvert train.ipynb --to python
   ```

2. Hydraは以下のコマンドで実行可能です
    ```sh
    >> python3 train.py model.hidden_size=24
    ```

3. MLFlowで結果を確認する  
    まずは mlrunsのあるディレクトリに移動
    ```sh
    >> cd outputs/2021-12-03/09-46-26 
    >> mlflow ui --port 5000
    ```