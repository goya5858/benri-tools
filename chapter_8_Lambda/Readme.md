Lambdaへのコンテナアプリのデプロイ

1. 使用するDockerImageのベースは  
    　public.ecr.aws/lambda/python:3.8  
    とする

2. working_dirは変更しない！！！

3. CMD [file名.function名]で設定する