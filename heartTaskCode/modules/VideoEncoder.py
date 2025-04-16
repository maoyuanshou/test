import copy
from typing import Tuple
import pytorch_lightning as pl
import torch
import torchvision

#视频编码器


# 模型输入维度不匹配时，自动添加维度
def _unsqueeze(x: torch.Tensor, target_dim: int, expand_dim: int) -> Tuple[torch.Tensor, int]:
    tensor_dim = x.dim()
    if tensor_dim == target_dim - 1:
        x = x.unsqueeze(expand_dim)
    elif tensor_dim != target_dim:
        raise ValueError(f"Unsupported input dimension {x.shape}")
    return x, tensor_dim


torch.fx.wrap("_unsqueeze")

# 视频编码器类：用于视图分类模型
class VideoEncoder(pl.LightningModule):
    #初始化函数，加载预训练模型
    def __init__(self, frozen=False):
        super(VideoEncoder, self).__init__()
        checkpoint = torch.load("./model_weight/echo_prime_encoder.pt", weights_only=True)
        self.echo_encoder = torchvision.models.video.mvit_v2_s()  # 这个是一个视频模型
        self.echo_encoder.head[-1] = torch.nn.Linear(self.echo_encoder.head[-1].in_features, 512)
        self.echo_encoder.load_state_dict(checkpoint)
        #self.echo_encoder.head[-1] = torch.nn.Linear(self.echo_encoder.head[-1].in_features, 512)
        for param in self.echo_encoder.parameters():
            param.requires_grad = False if frozen else True

    def forward(self, x):
        Videosfeatures = self.echo_encoder(x)
        return Videosfeatures

#多任务视频编码器：用于多任务模型
class VideoEncoderForMulti(pl.LightningModule):
    #初始化函数，加载预训练模型
    def __init__(self, frozen=True):
        super(VideoEncoderForMulti, self).__init__()
        # 加载预训练模型
        checkpoint = torch.load("./model_weight/echo_prime_encoder.pt", weights_only=True)
        echo_encoder = torchvision.models.video.mvit_v2_s()  # 视频模型
        echo_encoder.head[-1] = torch.nn.Linear(echo_encoder.head[-1].in_features, 512)
        echo_encoder.load_state_dict(checkpoint)
        # 根据参数冻结整个模型
        for param in echo_encoder.parameters():
            param.requires_grad = False if frozen else True

        self.conv_proj = echo_encoder.conv_proj
        self.pos_encoding = echo_encoder.pos_encoding
        self.blocks = echo_encoder.blocks
        self.norm = echo_encoder.norm
        self.head = echo_encoder.head

        # 创建新的可训练的 blocks[-1] 作为另一个分支
        self.trainableLastBlock = copy.deepcopy(self.blocks[-1])
        for param in self.trainableLastBlock.parameters():
            param.requires_grad = True  # 确保新块可训练

    def forward(self, x):
        # Convert if necessary (B, C, H, W) -> (B, C, 1, H, W)
        x = _unsqueeze(x, 5, 2)[0]
        # patchify and reshape: (B, C, T, H, W) -> (B, embed_channels[0], T', H', W') -> (B, THW', embed_channels[0])
        x = self.conv_proj(x)
        x = x.flatten(2).transpose(1, 2)

        # add positional encoding
        x = self.pos_encoding(x)

        # pass patches through the encoder
        block_before_last_x = None
        block_before_last_thw = None
        thw = (self.pos_encoding.temporal_size,) + self.pos_encoding.spatial_size
        for i, block in enumerate(self.blocks):
            x, thw = block(x, thw)
            if i == len(self.blocks) - 2:
                block_before_last_x = x  # 获取倒数第二个 block 的输出
                block_before_last_thw = thw

        feature_mi = self.norm(x)
        # classifier "token" as used by standard language architectures
        feature_mi = feature_mi[:, 0]
        feature_mi = self.head(feature_mi)

        feature_view, _ = self.trainableLastBlock(block_before_last_x, block_before_last_thw)

        feature_view = self.norm(feature_view)

        # classifier "token" as used by standard language architectures
        feature_view = feature_view[:, 0]
        feature_view = self.head(feature_view)

        return feature_view, feature_mi
