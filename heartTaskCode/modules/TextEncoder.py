import pytorch_lightning as pl
import torch
import torchvision
from open_clip import tokenize, create_model_and_transforms


class TextEncoder(pl.LightningModule):
    def __init__(self):
        super().__init__()
        echo_clip, _, _ = create_model_and_transforms(
            "hf-hub:mkaichristensen/echo-clip", device="cuda"
        )
        # if frozen:
        for param in echo_clip.parameters():
            param.requires_grad = False
        # else:
        #     for param in echo_clip.parameters():
        #         param.requires_grad = True
        self.transformer = echo_clip.encode_text

    def forward(self, x):
        text_embedding = self.transformer(x)
        return text_embedding
