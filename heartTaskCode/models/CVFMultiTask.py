import torch
import pytorch_lightning as pl
from modules import VideoEncoderForMulti, TextEncoder, MutiTask_MIClsMLP,MutiTask_ViewClsMLP, ViewAdapter, AttnFusion
import utils
from open_clip import tokenize

class CVFMultiTask(pl.LightningModule):
    def __init__(self, frozen=True):
        super().__init__()

        # 视频编码器和文本编码器
        self.videoEncoder = VideoEncoderForMulti(frozen)
        self.textEncoder = TextEncoder()

        # 切面适配器
        self.a2cAdapter = ViewAdapter(512, 256)
        self.a4cAdapter = ViewAdapter(512, 256)

        # 跨切面的自注意力融合
        self.crossViewAttnfusion = AttnFusion(layers=4)

        # 切面分类器
        self.viewMLP = MutiTask_ViewClsMLP(512, 1)
        # MI分类器
        self.miMLP = MutiTask_MIClsMLP(512, 1)

        # 冻结状态标志
        self.freeze_mi_task()

    def freeze_mi_task(self):
        # 冻结心梗诊断相关的参数 并且解冻编码器
        for param in self.miMLP.parameters():
            param.requires_grad = False
        for param in self.crossViewAttnfusion.parameters():
            param.requires_grad = False

    def unfreeze_mi_task(self):
        # 解冻心梗诊断相关的参数 冻结编码器 解冻倒数嵌入层
        for param in self.miMLP.parameters():
            param.requires_grad = True
        for param in self.crossViewAttnfusion.parameters():
            param.requires_grad = True


    def forward(self, video1, video2):

        # 获取视频特征
        video1ViewFeature, video1MIFeature = self.videoEncoder(video1)  # [batch_size, 512]
        video2ViewFeature, video2MIFeature = self.videoEncoder(video2)  # [batch_size, 512]

        # 切面分类任务：预测 video1 和 video2 属于 A2C 还是 A4C
        logit_view1, vx1_for_mi = self.viewMLP(video1ViewFeature)  # 分类预测 video1
        logit_view2, vx2_for_mi = self.viewMLP(video2ViewFeature)  # 分类预测 video2
        vx_for_mi = (vx1_for_mi + vx2_for_mi) / 2.0

        # 将 logits 转化为概率
        viewProb_video1 = torch.sigmoid(logit_view1)  # [batch_size, 1]
        viewProb_video2 = torch.sigmoid(logit_view2)  # [batch_size, 1]

        # 将 logits 转化为预测标签（大于0.5为1，反之为0）
        viewPred_video1 = (viewProb_video1 > 0.5).float()  # [batch_size, 1]
        viewPred_video2 = (viewProb_video2 > 0.5).float()  # [batch_size, 1]

        video1AdaptedFeature = torch.zeros_like(video1MIFeature)  # 初始化为零
        video2AdaptedFeature = torch.zeros_like(video2MIFeature)  # 初始化为零

        # 遍历每个样本，根据分类结果选择对应的嵌入
        for i in range(viewPred_video1.size(0)):
            if viewPred_video1[i] == 0:  # 分类结果是A2C
                video1AdaptedFeature[i] = self.a2cAdapter(video1MIFeature[i].unsqueeze(0)).squeeze(0)  # 适配后去掉多余维度
            else:  # 分类结果是A4C
                video1AdaptedFeature[i] = self.a4cAdapter(video1MIFeature[i].unsqueeze(0)).squeeze(0)  # 适配后去掉多余维度

            if viewPred_video2[i] == 0:  # 分类结果是A2C
                video2AdaptedFeature[i] = self.a2cAdapter(video2MIFeature[i].unsqueeze(0)).squeeze(0)  # 适配后去掉多余维度
            else:  # 分类结果是A4C
                video2AdaptedFeature[i] = self.a4cAdapter(video2MIFeature[i].unsqueeze(0)).squeeze(0)  # 适配后去掉多余维度

        # 结合视频特征
        stackedVideoFeature = torch.stack([video1AdaptedFeature, video2AdaptedFeature], dim=0)  # [2, batch_size, 512]
        # 跨切面的自注意力融合
        fusedFeatures = self.crossViewAttnfusion(stackedVideoFeature)

        # 使用最终的分类MLP输出结果
        logit_mi = self.miMLP(fusedFeatures, vx_for_mi)

        return logit_mi, logit_view1, logit_view2
