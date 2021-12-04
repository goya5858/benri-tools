#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from sklearn import datasets
import numpy as np

import torch
import pytorch_lightning as pl
from pytorch_lightning import LightningModule, Trainer, LightningDataModule
from torchmetrics import Accuracy
from torch import nn
from torch.nn import functional as F

from torch.utils.data import DataLoader, random_split
from torchvision import transforms

from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

import mlflow

from omegaconf import DictConfig, ListConfig, OmegaConf
import hydra


# # Writer@MLFlowの実装

# In[2]:


# 低レベルAPIでのMLFlowの使用

class MlflowWriter():
    def __init__(self, experiment_name):
        self.client = mlflow.tracking.MlflowClient()

        # 新規 experiment の作成
        try: 
            self.experiment_id = self.client.create_experiment(experiment_name)
        except Exception as e:
            print(e)
            self.experiment_id = self.client.get_experiment_by_name(experiment_name).experiment_id

        self.experiment = self.client.get_experiment(self.experiment_id)
        print("New experiment started")
        print(f"Name: {self.experiment.name}")
        print(f"Experiment_id: {self.experiment.experiment_id}")
        #print(f"Artifact Location: {self.experiment.artifact_location}")
    
    # 新規RUNの作成
    def create_new_run(self, tags=None):
        self.run = self.client.create_run(self.experiment_id, tags=tags)
        self.run_id = self.run.info.run_id
        #print(f"New run started: {tags['mlflow.runName']}")

    # OmegaConf形式のparamsを記録する
    def log_params_from_omegaconf_dict(self, params):
        for param_name, element in params.items():
            self._explore_recursive(param_name, element)
    def _explore_recursive(self, parent_name, element):
        if isinstance(element, DictConfig):
            for k, v in element.items():
                if isinstance(v, DictConfig) or isinstance(v, ListConfig):
                    self._explore_recursive(f'{parent_name}.{k}', v)
                else:
                    self.client.log_param(self.run_id, f'{parent_name}.{k}', v)
        elif isinstance(element, ListConfig):
            for i, v in enumerate(element):
                self.client.log_param(self.run_id, f'{parent_name}.{i}', v)
        else:
            self.client.log_param(self.run_id, f'{parent_name}', element)

    # 通常形式での保存メソッドのラッパー
    def log_param(self, key, value):
        self.client.log_param(self.run_id, key, value)
    def log_metric(self, key, value):
        self.client.log_metric(self.run_id, key, value)
    def log_metric_step(self, key, value, step): #stepアリの場合
        self.client.log_metric(self.run_id, key, value, step=step)
    def log_artifact(self, local_path):
        self.client.log_artifact(self.run_id, local_path)
    def log_dict(self, dictionary, file):
        self.client.log_dict(self.run_id, dictionary, file)
    def log_figure(self, figure, file):
        self.client.log_figure(self.run_id, figure, file)

    # 必ず終了時に呼び出す
    def set_terminated(self):
        self.client.set_terminated(self.run_id)


# # DataModuleの準備

# In[3]:


# 1. DataSetの作成
#   ここは従来通り、任意のデータに対応するDatasetを作成する
class IrisDataset(torch.utils.data.Dataset):
    def __init__(self, transforms=None):
        super().__init__()
        iris = datasets.load_iris()
        self.X, self.y = iris["data"], iris["target"]
        self.transforms = transforms

    def __getitem__(self, idx):
        data, label = self.X[idx], self.y[idx]
        if self.transforms is not None:
            data  = self.transforms(data)
            label = self.transforms(label)
        return data, label

    def __len__(self):
        return self.X.shape[0]


# In[4]:


# 2. pl.DataModuleの準備
#   DataLoadersを作成するpl.DataModuleを作成する

class PLIrisData(pl.LightningDataModule):
    def __init__(self, BATCH_SIZE=16):
        super().__init__()
        self.batch_size = BATCH_SIZE
        self.transforms=None
         #self.transforms = transforms.Compose( [ transforms.ToTensor() ] )  #画像などで使う
    
    def setup(self, stage=None): #stageの引数は必須　
        all_data = IrisDataset(transforms=self.transforms)
        self.trn_data, self.val_data = random_split(all_data, [120,30])
    
    def train_dataloader(self):
        return DataLoader( dataset=self.trn_data, batch_size=self.batch_size ,shuffle=True)
    
    def val_dataloader(self):
        return DataLoader( dataset=self.val_data, batch_size=self.batch_size ,shuffle=False)


# # Modelの作成

# In[5]:


# 1. 従来通りのModelを作成する

class IrisNet(nn.Module):
    def __init__(self, cfg):
        super().__init__()

        self.x1   = nn.Linear(in_features=4, out_features=cfg.model.hidden_size )
        self.act1 = nn.ReLU()
        self.x2   = nn.Linear(in_features=cfg.model.hidden_size, out_features=3)
        self.act2 = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.x1(x)
        x = self.act1(x)
        x = self.x2(x)
        x = self.act2(x)
        return x


# In[6]:


#2. train/valid stepを設定する、plmoduleを作成する

class PLIrisModel(pl.LightningModule):
    def __init__(self, cfg: DictConfig, experiment_name="test1"):
        super().__init__()
        self.cfg     = cfg

        self.net     = IrisNet(cfg=cfg)
        self.mtrics  = Accuracy()

        ### MLFlow ###
        self.writer = MlflowWriter(experiment_name=experiment_name)
        self.writer.create_new_run()
        self.writer.log_params_from_omegaconf_dict(cfg)

    def forward(self, x):
        return self.net(x.float())

    def training_step(self, batch, batch_idx):
        x, y = batch
        pred = self(x)
        loss = F.nll_loss(pred, y)
        batch_loss = loss * x.size(0)
        return {"loss": loss, "y": y, "pred": pred.detach(), "batch_loss": batch_loss.detach()}
    
    def training_epoch_end(self, train_step_outputs):
        preds      = torch.cat( [trn["pred"] for trn in train_step_outputs], dim=0 )
        ys         = torch.cat( [trn["y"] for trn in train_step_outputs], dim=0 )
        epoch_loss = sum( [trn["batch_loss"] for trn in train_step_outputs] ) / ys.size(0)

        acc = self.mtrics(preds, ys)
        print('-------- Current Epoch {} --------'.format(self.current_epoch + 1))
        print('train Loss: {:.4f} train Acc: {:.4f}'.format(epoch_loss, acc))

        ### MLFlow ###
        self.writer.log_metric("trn_loss", float(epoch_loss) )
        self.writer.log_metric("trn_acc",  float(acc))

    def validation_step(self, batch, batch_idx):
        x, y = batch
        pred = self(x)
        loss = F.nll_loss(pred, y)
        batch_loss = loss * x.size(0)
        return {"y": y, "pred": pred.detach(), "batch_loss": batch_loss.detach()}
    
    def validation_epoch_end(self, valid_step_outputs):
        preds      = torch.cat( [val["pred"] for val in valid_step_outputs], dim=0 )
        ys         = torch.cat( [val["y"] for val in valid_step_outputs], dim=0 )
        epoch_loss = sum( [val["batch_loss"] for val in valid_step_outputs] ) / ys.size(0)

        acc = self.mtrics(preds, ys)
        print('-------- Current Epoch {} --------'.format(self.current_epoch + 1))
        print('valid Loss: {:.4f} valid Acc: {:.4f}'.format(epoch_loss, acc))

        ### for CallBacks ###
        self.log("val_loss", epoch_loss)
        self.log("val_acc", acc)
        
        ### MLFlow ###
        self.writer.log_metric("val_loss", float(epoch_loss) )
        self.writer.log_metric("val_acc",  float(acc))
    
    def configure_optimizers(self):
        lr         = self.cfg.optim.lr
        optim_name = self.cfg.optim.optim_name
        optimizer  = getattr(torch.optim, optim_name)(self.parameters(), lr=lr)
        return optimizer


# In[8]:


# CallBacksの設定

# モデルチェックポイント val_lossが最低となるモデルを保存
checkpoint_callback = ModelCheckpoint(
        dirpath=f"./models",
        filename="best-checkpoint",
        monitor="val_loss",
        mode="min",
    )

# EarlyStop 一定エポックval_lossの改善がなければ学習打ち切り
early_stopping_callback = EarlyStopping(
        monitor="val_loss", patience=3, verbose=True, mode="min"
    )


# In[9]:


#cfg = OmegaConf.load("configs/config.yaml")

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


# In[ ]:


main()

