import torch
from torch import nn

# 辅助函数们，应该是原来的代码中用到的一些函数，现在应该都没用到

# 确定下降的路径：以存活率survival_rate为根据，确定随机的下降深度
def drop_path(x, drop_prob: float = 0., training: bool = False):
    """Drop paths (Stochastic Depth) per sample (when applied in main path of residual blocks).
  This is the same as the DropConnect impl I created for EfficientNet, etc networks, however,
  the original name is misleading as 'Drop Connect' is a different form of dropout in a separate paper...
  See discussion: https://github.com/tensorflow/tpu/issues/494#issuecomment-532968956 ... I've opted for
  changing the layer and argument names to 'drop path' rather than mix DropConnect as a layer name and use
  'survival rate' as the argument.
  """
    if drop_prob == 0. or not training:
        return x
    keep_prob = 1 - drop_prob
    shape = (x.shape[0],) + (1,) * (x.ndim - 1)  # work with diff dim tensors, not just 2D ConvNets
    random_tensor = keep_prob + torch.rand(shape, dtype=x.dtype, device=x.device)
    random_tensor.floor_()  # binarize
    output = x.div(keep_prob) * random_tensor
    return output

# 下降路径类，和上面函数功能一样，但是这里是一个类（方便forward）
class DropPath(nn.Module):
    """Drop paths (Stochastic Depth) per sample  (when applied in main path of residual blocks).
  """

    def __init__(self, drop_prob=None):
        super(DropPath, self).__init__()
        self.drop_prob = drop_prob

    def forward(self, x):
        return drop_path(x, self.drop_prob, self.training)

# 激活函数QuickGELU
class QuickGELU(nn.Module):
    def forward(self, x: torch.Tensor):
        return x * torch.sigmoid(1.702 * x)

# 分割用的prompt，这里估计是原始代码还包括了一些语义分割的任务和多模态，现在应该是用不到
segment_prompts = {
    "A2C": ['ATHEROSCLEROTIC HEART DISEASE OF NATIVE CORONARY ARTERY WITHOUT ANGINA PECTORIS.'
        , 'THERE IS THE POSSIBILITY OF A LEFT VENTRICULAR APICAL MURAL THROMBUS.'
        , 'THERE IS <#> (><#>MM) ATHEROMA OF THE THORCIC AORTA. '
        , 'THERE ARE NO REGIONAL WALL MOTION ABNORMALITIES. '
        , 'THERE IS GLOBAL LEFT VENTRICULAR HYPOKINESIS. '
        , 'RESTING SEGMENTAL WALL MOTION ANALYSIS. '
        , 'WALL MOTION ABNORMALITIES HAVE RESOLVED'
        , 'NORMAL LEFT VENTRICULAR WALL THICKNESS.'
        , 'WALL MOTION ABNORMALITIES UNCHANGED'
        , 'WALL MOTION ABNORMALITIES ARE NEW'
        , 'TOTAL WALL MOTION SCORE IS <#>. '
        , 'BASAL TO MID ANTEROSEPTAL WALL.'
        , 'LV EJECTION FRACTION IS <#>%.'
        , 'AORTIC VALVE SCLEROSIS SEEN.'
        , 'WALL THICKNESS HAS DECREASED'
        , 'WALL THICKNESS HAS INCREASED'
        , 'WALL THICKNESS IS UNCHANGED'
        , 'THERE IS HYPOKINESIS OF THE'
        , 'BASAL TO MID INFERIOR WALL.'
        , 'ENTIRE INFEROLATERAL WALL.'
        , 'THERE IS DYSKINESIS OF THE'
        , 'OLD MYOCARDIAL INFARCTION.'
        , 'ATHEROMA THICKNESS <#>MM.'
        , 'CORONARY ARTERY DISEASE.'
        , "The basal anterior wall demonstrates abnormal motion."
        , "The mid anterior wall demonstrates abnormal motion."
        , "The apical anterior wall demonstrates abnormal motion."
        , "The apical cap demonstrates abnormal motion."
        , "The apical inferior wall demonstrates abnormal motion."
        , "The mid inferior wall demonstrates abnormal motion."
        , "The basal inferior wall demonstrates abnormal motion."
        , "There is abnormal regional wall motion"
        , "There is global hypokinesis with regional variation."
            ],
    "A4C": ['ATHEROSCLEROTIC HEART DISEASE OF NATIVE CORONARY ARTERY WITHOUT ANGINA PECTORIS.'
        , 'THERE IS THE POSSIBILITY OF A LEFT VENTRICULAR APICAL MURAL THROMBUS.'
        , 'THERE IS <#> (><#>MM) ATHEROMA OF THE THORCIC AORTA. '
        , 'THERE ARE NO REGIONAL WALL MOTION ABNORMALITIES. '
        , 'THERE IS GLOBAL LEFT VENTRICULAR HYPOKINESIS. '
        , 'RESTING SEGMENTAL WALL MOTION ANALYSIS. '
        , 'WALL MOTION ABNORMALITIES HAVE RESOLVED'
        , 'NORMAL LEFT VENTRICULAR WALL THICKNESS.'
        , 'WALL MOTION ABNORMALITIES UNCHANGED'
        , 'WALL MOTION ABNORMALITIES ARE NEW'
        , 'TOTAL WALL MOTION SCORE IS <#>. '
        , 'BASAL TO MID ANTEROSEPTAL WALL.'
        , 'LV EJECTION FRACTION IS <#>%.'
        , 'AORTIC VALVE SCLEROSIS SEEN.'
        , 'WALL THICKNESS HAS DECREASED'
        , 'WALL THICKNESS HAS INCREASED'
        , 'WALL THICKNESS IS UNCHANGED'
        , 'THERE IS HYPOKINESIS OF THE'
        , 'BASAL TO MID INFERIOR WALL.'
        , 'ENTIRE INFEROLATERAL WALL.'
        , 'THERE IS DYSKINESIS OF THE'
        , 'OLD MYOCARDIAL INFARCTION.'
        , 'ATHEROMA THICKNESS <#>MM.'
        , 'CORONARY ARTERY DISEASE.'
        , "The basal inferoseptal wall demonstrates abnormal motion."
        , "The mid inferoseptal wall demonstrates abnormal motion."
        , "The apical septal wall demonstrates abnormal motion."
        ,  "The apical cap demonstrates abnormal motion."
        ,  "The apical lateral wall demonstrates abnormal motion."
        ,  "The mid anterolateral wall demonstrates abnormal motion."
        ,  "The basal anterolateral wall demonstrates abnormal motion."
        , "There is abnormal regional wall motion"
        , "There is global hypokinesis with regional variation."
            ]
}

related_prompts = ['ATHEROSCLEROTIC HEART DISEASE OF NATIVE CORONARY ARTERY WITHOUT ANGINA PECTORIS.'
    , 'THERE IS THE POSSIBILITY OF A LEFT VENTRICULAR APICAL MURAL THROMBUS.'
    , 'THERE IS <#> (><#>MM) ATHEROMA OF THE THORCIC AORTA. '
    , 'THERE ARE NO REGIONAL WALL MOTION ABNORMALITIES. '
    , 'THERE IS GLOBAL LEFT VENTRICULAR HYPOKINESIS. '
    , 'RESTING SEGMENTAL WALL MOTION ANALYSIS. '
    , 'WALL MOTION ABNORMALITIES HAVE RESOLVED'
    , 'NORMAL LEFT VENTRICULAR WALL THICKNESS.'
    , 'WALL MOTION ABNORMALITIES UNCHANGED'
    , 'WALL MOTION ABNORMALITIES ARE NEW'
    , 'TOTAL WALL MOTION SCORE IS <#>. '
    , 'BASAL TO MID ANTEROSEPTAL WALL.'
    , 'LV EJECTION FRACTION IS <#>%.'
    , 'AORTIC VALVE SCLEROSIS SEEN.'
    , 'WALL THICKNESS HAS DECREASED'
    , 'WALL THICKNESS HAS INCREASED'
    , 'WALL THICKNESS IS UNCHANGED'
    , 'THERE IS HYPOKINESIS OF THE'
    , 'BASAL TO MID INFERIOR WALL.'
    , 'ENTIRE INFEROLATERAL WALL.'
    , 'THERE IS DYSKINESIS OF THE'
    , 'OLD MYOCARDIAL INFARCTION.'
    , 'ATHEROMA THICKNESS <#>MM.'
    , 'CORONARY ARTERY DISEASE.'
                   ]
