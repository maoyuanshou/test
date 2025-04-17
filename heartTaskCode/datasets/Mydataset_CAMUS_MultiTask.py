import csv
import random
import torch
import torchvision
from . import video_utils

class Mydataset_CAMUS_Multitask(torchvision.datasets.VisionDataset):
    def __init__(self, split, fold):
        '''
        HMC数据集 用echoclip的预处理
        根据标签选择出完整心动周期的帧序列
        按照时间比例抽出16帧 如果是both 会返回两个切面的tensor
        :param split: 属于哪个划分train or test
        :param fold: 属于哪一折 1024代表全部
        '''
        super().__init__()
        self.split = split
        self.patients = []
        self.segs = []
        subfile = './metafiles/label_select160.csv'
        self.heartFrames = []
        if fold != 1024:
            with open(subfile) as mfile:
                reader = csv.DictReader(mfile, delimiter=',')
                for row in reader:
                    if (split == "train" and fold != int(row['fold'])) or (
                            split == "test" and fold == int(row['fold'])):
                        self.patients.append(row['Number'])
                        seg = int(row["Both"])
                        self.heartFrames.append(
                            (int(row["Start_A2C"]), int(row["End_A2C"]), int(row["Start_A4C"]), int(row["End_A4C"])))
                        self.segs.append(seg)

        else:
            with open(subfile) as mfile:
                reader = csv.DictReader(mfile, delimiter=',')
                for row in reader:
                    self.patients.append(row['Number'])
                    seg = int(row["Both"])
                    self.heartFrames.append(
                        (int(row["Start_A2C"]), int(row["End_A2C"]), int(row["Start_A4C"]), int(row["End_A4C"])))
                    self.segs.append(seg)

    def __len__(self):
        return len(self.patients)

    def __getitem__(self, idx):
        # 加载视频并提取 num_frames 帧
        name = self.patients[idx]
        segs = self.segs[idx]
        heartFrames = self.heartFrames[idx]

        a2c_path = f'/root/autodl-tmp/heartTaskCode/CAMUS-被省医院医生标注了心肌梗死标签/A2C/{name}.avi'
        tensor1 = video_utils.process_avi_videos(a2c_path, heartFrames[0], heartFrames[1])

        a4c_path = f'/root/autodl-tmp/heartTaskCode/CAMUS-被省医院医生标注了心肌梗死标签/A4C/{name}.avi'
        tensor2 = video_utils.process_avi_videos(a4c_path, heartFrames[2], heartFrames[3])
        # 创建切面分类标签
        labels = [0, 1]  # A2C为0，A4C为1

        # 随机交换顺序
        if random.random() > 0.5:
            tensor1, tensor2 = tensor2, tensor1
            labels = [1, 0]  # 如果交换，更新标签顺序

        # 返回数据
        return (tensor1, tensor2), {"View_label": labels, "MI_label": segs}
