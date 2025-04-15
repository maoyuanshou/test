from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from datasets import Mydataset_Sichuan_ViewCls
from model import MyModel_View_CLS_Video
import torch


if __name__ == '__main__':
    train_dataset = Mydataset_Sichuan_ViewCls(r"D:\dataset\shengyiyuan\切面分类\train.txt")
    test_dataset = Mydataset_Sichuan_ViewCls(r"D:\dataset\shengyiyuan\切面分类\test.txt")

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=4, shuffle=True,
        num_workers=0, pin_memory=True)

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=4, shuffle=False,
        num_workers=0, pin_memory=True)
    accs = []
    f1s = []
    specs = []
    precs = []
    recs = []

    # 使用 checkpoint 继续训练
    checkpoint_callback = ModelCheckpoint(
        dirpath="./checkpoint",  # 保存路径
        filename="viewCls-checkpoint",  # 文件名格式
        save_top_k=1,  # 只保存最好的模型
        verbose=True,
        monitor="val_loss",  # 监控的指标
        mode="min"  # "min" 表示最小化该指标
    )

    trainer = Trainer(max_epochs=1000, gpus=[0], callbacks=[checkpoint_callback], check_val_every_n_epoch=1)
    model = MyModel_View_CLS_Video(1e-5)
    trainer.fit(model, train_dataloader, test_dataloader)
    # 测试模型
    metrics = trainer.logged_metrics
    accs.append(metrics['val_acc'])
    f1s.append(metrics['val_f1'])
    specs.append(metrics['val_spec'])
    precs.append(metrics['val_prec'])
    recs.append(metrics['val_rec'])
    print('Average metrics\n')
    print('Accuracy:', sum(accs))
    print('F1:', sum(f1s) )
    print('Specificity:', sum(specs))
    print('Precision:', sum(precs)  )
    print('Sensitivity:', sum(recs))
