import torch.nn as nn
import pytorch_lightning as pl
import torch


class ClsMLP(pl.LightningModule):
    def __init__(self, input_size, output_size, dropout_prob=0.5):
        super(ClsMLP, self).__init__()

        # 第一层全连接层，输入大小为 input_size，输出大小为 256
        self.fc1 = nn.Linear(input_size, 256)
        self.dropout = nn.Dropout(dropout_prob)  # Dropout 层

        # 输出层，输入大小为 256，输出大小为 output_size
        self.fc2 = nn.Linear(256, output_size)

        self.relu = nn.ReLU()  # ReLU 激活函数

    def forward(self, x):
        x = self.relu(self.fc1(x))  # 第一层全连接层 + ReLU 激活
        x = self.dropout(x)  # Dropout
        x = self.fc2(x)  # 输出层
        return x


class MutiTask_ViewClsMLP(pl.LightningModule):
    def __init__(self, input_size, output_size, dropout_prob=0.5):
        super(MutiTask_ViewClsMLP, self).__init__()

        self.fc1 = nn.Linear(input_size, 256)  # 第二个全连接层，输入大小为 512，输出大小为 256
        self.dropout1 = nn.Dropout(dropout_prob)  # Dropout 层

        self.fc2 = nn.Linear(256, output_size)  # 输出层，输入大小为 256，输出大小为 output_size

        self.relu = nn.ReLU()  # ReLU 激活函数0

    def forward(self, x):
        x_for_mi = self.relu(self.fc1(x))  # 第一层全连接层 + ReLU 激活
        x = self.dropout1(x_for_mi)  # 第一层 Dropout
        x = self.fc2(x)  # 输出层
        return x, x_for_mi


class MutiTask_MIClsMLP(pl.LightningModule):
    def __init__(self, input_size, output_size, dropout_prob=0.5):
        super(MutiTask_MIClsMLP, self).__init__()

        self.fc1 = nn.Linear(input_size, 256)  # 第二个全连接层，输入大小为 512，输出大小为 256
        self.dropout1 = nn.Dropout(dropout_prob)  # Dropout 层
        self.dropout2 = nn.Dropout(dropout_prob)  # Dropout 层
        self.fc2 = nn.Linear(256 + 256, 256)  # 输出层，输入大小为 256，输出大小为 output_size
        self.fc3 = nn.Linear(256, output_size)  # 输出层，输入大小为 256，输出大小为 output_size
        self.relu = nn.ReLU()  # ReLU 激活函数0


    def forward(self, x, x_for_mi):
        x_ori = x
        x = self.relu(self.fc1(x))  # 第一层全连接层 + ReLU 激活 输出256
        x = torch.cat((x, x_for_mi), 1) + x_ori #拼成 512
        x = self.dropout1(x)# 第一层 Dropout
        x = self.relu(self.fc2(x))# 输出层
        x = self.dropout2(x)  #加了残差
        x = self.fc3(x)
        return x



