import torch
import torch.nn as nn

class ViewAdapter(nn.Module):
    def __init__(self, input_dim, adapter_dim):
        super(ViewAdapter, self).__init__()
        # 降维层，将输入从高维度 input_dim 降到 adapter_dim
        self.down_project = nn.Linear(input_dim, adapter_dim)
        # 非线性激活函数
        self.activation = nn.ReLU()
        # 升维层，将特征从 adapter_dim 升回原来的 input_dim
        self.up_project = nn.Linear(adapter_dim, input_dim)

    def forward(self, x):
        # 残差连接：输入通过降维、激活、升维，然后加回原始输入
        residual = x
        x = self.down_project(x)
        x = self.activation(x)
        x = self.up_project(x)
        return x + residual  # 这里是残差连接

class TextAdapter(nn.Module):
    def __init__(self, input_dim, adapter_dim):
        super(TextAdapter, self).__init__()
        # 降维层，将输入从高维度 input_dim 降到 adapter_dim
        self.down_project = nn.Linear(input_dim, adapter_dim)
        # 非线性激活函数
        self.activation = nn.ReLU()
        # 升维层，将特征从 adapter_dim 升回原来的 input_dim
        self.up_project = nn.Linear(adapter_dim, input_dim)

    def forward(self, x):
        # 残差连接：输入通过降维、激活、升维，然后加回原始输入
        residual = x
        x = self.down_project(x)
        x = self.activation(x)
        x = self.up_project(x)
        return x + residual  # 这里是残差连接
