Optunaのデモ用のページです  

1. train_Optuna.ipynb :  
最もシンプルな実装です


2. train_Optuna_MLFlow.ipynb :   
Optuna加えて、低レベルAPIでのMLFlowの実装です  
最後のセルを実行することでMLFlowで各パラメーターでの結果を確認することができます

3. train_Optuna_MLFlow_Hydra.py :    
上記に加えてHydraを加えた実装です  
Hydraの通常の実行法でモデルの学習が可能です
    ```
    >> python3 train_Optuna_MLFlow_Hydra.py
    ```
    3.5.　MLFlowでの確認  
    　　まずは mlrunsのあるディレクトリに移動
    ```sh
    >> cd outputs/2021-12-03/09-46-26 
    >> mlflow ui --port 5000
    ```