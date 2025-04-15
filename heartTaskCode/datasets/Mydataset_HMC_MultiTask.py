import csv
import random
import torchvision
from . import video_utils


class Mydataset_HMC_MultiTask(torchvision.datasets.VisionDataset):
    def __init__(self, split, fold):
        '''
        HMC数据集，用于多任务（切面分类和诊断任务）
        同时处理 A2C 和 A4C 两个切面，返回分类标签和分割标签。

        :param split: 属于哪个划分 train or test
        :param fold: 属于哪一折，1024代表全部
        '''
        super().__init__()
        self.split = split
        self.patients = []
        self.segs = []
        self.heartFrames = []
        subfile = './metafiles/160version.csv'

        if fold != 1024:
            with open(subfile) as mfile:
                reader = csv.DictReader(mfile, delimiter=',')
                for row in reader:
                    if (split == "train" and fold != int(row['fold'])) or (
                            split == "test" and fold == int(row['fold'])):
                        self.patients.append(row['name'])
                        seg = int(row["seg_Bi"])
                        self.heartFrames.append(
                            (int(row["RF_A2C"]), int(row["EC_A2C"]), int(row["RF_A4C"]), int(row["EC_A4C"])))
                        self.segs.append(seg)
        else:
            with open(subfile) as mfile:
                reader = csv.DictReader(mfile, delimiter=',')
                for row in reader:
                    self.patients.append(row['name'])
                    seg = int(row["seg_Bi"])
                    self.heartFrames.append(
                        (int(row["RF_A2C"]), int(row["EC_A2C"]), int(row["RF_A4C"]), int(row["EC_A4C"])))
                    self.segs.append(seg)

    def __len__(self):
        return len(self.patients)

    def __getitem__(self, idx):
        # 加载视频并提取帧
        name = self.patients[idx]
        segs = self.segs[idx]
        heartFrames = self.heartFrames[idx]

        # 加载 A2C 和 A4C 切面视频
        a2c_path = f'D:/dataset/HMC-QU/data_processed/data_ori_changename/A2C/{name}.avi'
        tensor1 = video_utils.process_avi_videos(a2c_path, heartFrames[0], heartFrames[1])

        a4c_path = f'D:/dataset/HMC-QU/data_processed/data_ori_changename/A4C/{name}.avi'
        tensor2 = video_utils.process_avi_videos(a4c_path, heartFrames[2], heartFrames[3])

        # 创建切面分类标签
        labels = [0, 1]  # A2C为0，A4C为1

        # 随机交换顺序
        if random.random() > 0.5:
            tensor1, tensor2 = tensor2, tensor1
            labels = [1, 0]  # 如果交换，更新标签顺序

        # 返回数据
        return (tensor1, tensor2), {"View_label": labels, "MI_label": segs}
