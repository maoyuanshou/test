import torch
import pytorch_lightning as pl
from modules import VideoEncoder, ClsMLP

# 视图分类模型的流程

class ViewClsModel(pl.LightningModule):
    def __init__(self, clsNum = 8):
        super().__init__()
        self.features = VideoEncoder()
        self.mlp = ClsMLP(input_size=512, output_size=clsNum)
    def forward(self, x):
        features = self.features(x)
        logit = self.mlp(features)
        return logit