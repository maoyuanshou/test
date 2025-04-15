import os
from torch.utils.data import Dataset
import pandas as pd
from . import video_utils

class Mydataset_Sichuan_ViewCls(Dataset):
    def __init__(self, txt_file):
        self.video_dir = r"D:\dataset\shengyiyuan\切面分类\processed"
        # 从 txt 文件读取文件名和标签
        self.data = pd.read_csv(txt_file, sep=' ', header=None, names=['file_name', 'label'])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # 获取文件名和标签
        video_file = self.data.iloc[idx, 0]
        label = self.data.iloc[idx, 1]

        # 生成视频的完整路径
        video_path = os.path.join(self.video_dir, video_file)
        video_tensor = video_utils.process_avi_videos(video_path, 1, 16)

        return video_tensor, label

