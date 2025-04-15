import torch
from torch import nn
from collections import OrderedDict
from timm.models.layers import trunc_normal_
import pytorch_lightning as pl
class QuickGELU(pl.LightningModule):
    def forward(self, x: torch.Tensor):
        return x * torch.sigmoid(1.702 * x)
class ResidualAttentionBlock(pl.LightningModule):
    def __init__(self, d_model: int, n_head: int):
        super().__init__()

        self.attn = nn.MultiheadAttention(d_model, n_head)
        self.ln_1 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(OrderedDict([
            ("c_fc", nn.Linear(d_model, d_model * 4)),
            ("gelu", QuickGELU()),
            ("c_proj", nn.Linear(d_model * 4, d_model))
        ]))
        self.ln_2 = nn.LayerNorm(d_model)

    def attention(self, x: torch.Tensor):
        return self.attn(x, x, x, need_weights=False, attn_mask=None)[0] #返回注意力输出 不要注意力权重

    def forward(self, x: torch.Tensor):
        x = x + self.attention(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x

class AttnFusion(pl.LightningModule):#加入cls_token
    def __init__(self, viewCount=2, embed_dim=512, layers=1):
        super().__init__()
        transformer_heads = embed_dim // 64

        # cls_token 初始化
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))

        # 位置嵌入初始化
        self.positional_embedding = nn.Parameter(torch.empty(viewCount + 1, 1, embed_dim))  # +1 是为了包含 cls_token 的位置嵌入
        trunc_normal_(self.positional_embedding, std=0.02)

        # Transformer 层
        self.resblocks = nn.Sequential(
            *[ResidualAttentionBlock(d_model=embed_dim, n_head=transformer_heads) for _ in range(layers)]
        )

    def forward(self, x):
        # 将 cls_token 加入到输入的开头
        batch_size = x.size(1)
        cls_tokens = self.cls_token.expand(1, batch_size, -1)  # (1, batch_size, embed_dim)
        x = torch.cat([cls_tokens, x], dim=0)  # (viewCount + 1, batch_size, embed_dim)

        # 加入位置嵌入
        ori_x = x
        x = x + self.positional_embedding
        x = self.resblocks(x)

        # 将 cls_token 的输出作为最终的聚合特征
        x = x[0]  # 取出 cls_token 表示的部分
        return x.type(ori_x.dtype)
