import torch
import pytorch_lightning as pl
import wandb
from datasets import Mydataset_CAMUS_Multitask
from model import MyModel_MultiTask
import argparse
import random
import numpy as np
from pytorch_lightning.callbacks import ModelCheckpoint
wandb.login()
parser = argparse.ArgumentParser(description='Process arguments')
parser.add_argument('--gpu', type=int, default=0)
parser.add_argument('--epochs', type=int, default= 1000)
parser.add_argument('--lr', type=float, default=1e-5)
parser.add_argument('--view', type=str, default='both')
parser.add_argument('--experimentName', type=str, default='CAMUS_CVF+多任务')
args = parser.parse_args()
print(args)


def fix_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


fix_seed(3407)
gpu = args.gpu
lr = args.lr
view = args.view
epochs = args.epochs
experimentName = args.experimentName

seg = None

view_accs = []
view_f1s = []
view_specs = []
view_precs = []
view_recs = []
view_aucs = []


mi_accs = []
mi_f1s = []
mi_specs = []
mi_precs = []
mi_recs = []
mi_aucs = []

class ConditionalCheckpoint(ModelCheckpoint):
    def __init__(self, start_epoch=80, **kwargs):
        super().__init__(**kwargs)
        self.start_epoch = start_epoch

    def on_train_epoch_end(self, trainer, pl_module):
        # 仅在 epoch >= start_epoch 时启用保存逻辑
        if trainer.current_epoch >= self.start_epoch:
            super().on_train_epoch_end(trainer, pl_module)

# 创建 ConditionalCheckpoint 回调

for fold in range(1, 2):
    print('fold', fold)

    train_dataset = Mydataset_CAMUS_Multitask(split="train", fold=fold)
    test_dataset = Mydataset_CAMUS_Multitask(split="test", fold=fold)

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=16, shuffle=True,
        num_workers=0, pin_memory=True)

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=16, shuffle=False,
        num_workers=0, pin_memory=True)

    # 初始化 WandB
    wandb_logger = pl.loggers.WandbLogger(
        project='心脏实验',  # 替换为你的项目名
        name=f'fold_{fold}_experiment_{experimentName}')  # 可自定义实验名称

    checkpoint_callback = ConditionalCheckpoint(
        monitor='val_acc_mi',  # 监控指标
        dirpath='checkpoints/',  # 保存路径
        filename=experimentName+str(fold)+'model-{epoch:02d}-{val_acc_mi:.2f}',  # 文件名格式
        save_top_k=1,  # 仅保存最好的模型
        mode='max',  # 指定监控指标是最小化
        start_epoch=81# 从第 80 个 epoch 开始保存
    )

    trainer = pl.Trainer(max_epochs=epochs, gpus=[gpu],
                         check_val_every_n_epoch=1, logger=wandb_logger,callbacks=[checkpoint_callback])
    model = MyModel_MultiTask(mlr=lr)
    trainer.fit(model, train_dataloader, test_dataloader)

    view_metrics = model.best_acc_metrics_view
    view_accs.append(view_metrics['val_acc_view'])
    view_f1s.append(view_metrics['val_f1_view'])
    view_specs.append(view_metrics['val_spec_view'])
    view_precs.append(view_metrics['val_prec_view'])
    view_recs.append(view_metrics['val_rec_view'])
    view_aucs.append(view_metrics['val_auc_view'])

    mi_metrics = model.best_acc_metrics_mi
    mi_accs.append(mi_metrics['val_acc_mi'])
    mi_f1s.append(mi_metrics['val_f1_mi'])
    mi_specs.append(mi_metrics['val_spec_mi'])
    mi_precs.append(mi_metrics['val_prec_mi'])
    mi_recs.append(mi_metrics['val_rec_mi'])
    mi_aucs.append(mi_metrics['val_auc_mi'])

    # 结束当前的 WandB 会话
    wandb.finish()

print('Average view over the 5 folds:\n')
print('Accuracy:', sum(view_accs) / 5)
print('F1:', sum(view_f1s) / 5)
print('Specificity:', sum(view_specs) / 5)
print('Precision:', sum(view_precs) / 5)
print('Sensitivity:', sum(view_recs) / 5)
print('AUC:', sum(view_aucs) / 5)


print('Average mi over the 5 folds:\n')
print('Accuracy:', sum(mi_accs) / 5)
print('F1:', sum(mi_f1s) / 5)
print('Specificity:', sum(mi_specs) / 5)
print('Precision:', sum(mi_precs) / 5)
print('Sensitivity:', sum(mi_recs) / 5)
print('AUC:', sum(mi_aucs) / 5)
