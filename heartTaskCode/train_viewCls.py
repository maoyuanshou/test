from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from datasets import Mydataset_Sichuan_ViewCls
from model import MyModel_View_CLS_Video
import torch
import os


if __name__ == '__main__':
    train_dataset = Mydataset_Sichuan_ViewCls(r"/root/autodl-tmp/heartTaskCode/切面分类/train.txt")
    test_dataset = Mydataset_Sichuan_ViewCls(r"/root/autodl-tmp/heartTaskCode/切面分类/test.txt")

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=4, shuffle=True,
        num_workers=13, pin_memory=True)

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=4, shuffle=False,
        num_workers=13, pin_memory=True)
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

    trainer = Trainer(max_epochs=5, gpus=[0], callbacks=[checkpoint_callback], check_val_every_n_epoch=1)
    model = MyModel_View_CLS_Video(1e-5)
    trainer.fit(model, train_dataloader, test_dataloader)
    model.plot_metrics() # 训练结束后画图，存成metrics_xxxxx.png
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

    # onnx导出测试
     # 加载最优模型
    best_model_path = checkpoint_callback.best_model_path
    best_model = MyModel_View_CLS_Video.load_from_checkpoint(best_model_path)
    best_model.eval()

    # 创建一个虚拟输入，用于 ONNX 导出
    dummy_input = torch.randn(1, 3, 16, 224, 224)  # 根据实际情况调整输入形状

    # 导出为 ONNX 格式
    onnx_path = os.path.join("./onnx", "viewCls-model.onnx")
    torch.onnx.export(
        best_model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=13,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )

    print(f"Model exported to {onnx_path}")

