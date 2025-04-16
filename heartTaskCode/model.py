import torch
import torch.nn as nn
import pytorch_lightning as pl
import torchmetrics
import madgrad
from models import CVFMultiTask, ViewClsModel
import time
import matplotlib.pyplot as plt
from datetime import datetime

class MyModel_View_CLS_Video(pl.LightningModule):  #根据需要替换model部分
    def __init__(self, mlr=1e-6):
        super().__init__()
        self.model = ViewClsModel()
        self.learning_rate = mlr
        self.BCEcriterion = nn.BCEWithLogitsLoss()

        # 初始化 torchmetrics 的指标
        self.spec = torchmetrics.Specificity(task='multiclass', num_classes=8, average='macro')
        self.f1 = torchmetrics.F1Score(task='multiclass', num_classes=8, average='macro')
        self.prec = torchmetrics.Precision(task='multiclass', num_classes=8, average='macro')
        self.rec = torchmetrics.Recall(task='multiclass', num_classes=8, average='macro')
        self.acc = torchmetrics.Accuracy(task='multiclass', num_classes=8)

        # 绘图数据存储
        self.train_losses = []
        self.train_accs = []
        self.val_losses = []
        self.val_accs = []
        # 存训练和测试时间
        self.train_epoch_start_time = 0
        self.validation_epoch_start_time = 0


    def forward(self, x):
        logits = self.model(x)
        return logits

    # epoch开始前存一个时间
    def on_train_epoch_start(self):
        self.train_epoch_start_time = time.time()
    
    # epoch结束后再记录一下时间，减最初的时间就是这一个epoch的时间
    def on_train_epoch_end(self):
        epoch_time = time.time() - self.train_epoch_start_time
        print(f"Epoch {self.current_epoch} Training Time: {epoch_time:.2f}s")
                # # 存一下这一个epoch的loss和acc，方便最后画图
        train_loss = self.trainer.callback_metrics.get("train_loss")
        train_acc = self.trainer.callback_metrics.get("train_acc")
        if train_loss: 
            self.train_losses.append(train_loss.item())
        if train_acc: 
            self.train_accs.append(train_acc.item())

    def training_step(self, batch, batch_idx):
        images, labels = batch
        labels = labels.long()  # Ensure labels are Long type
        outputs = self(images)
        loss = nn.CrossEntropyLoss()(outputs, labels)
        preds = torch.argmax(outputs, dim=1)

        # Calculate and log training metrics

        acc = self.acc(preds, labels)
        self.log("train_loss", loss)
        self.log("train_acc", acc, on_step=False,
                 on_epoch=True, prog_bar=True, logger=True)
        return loss
    # 测试epoch前记录一个时间
    def validation_epoch_start(self):
        self.validation_epoch_start_time = time.time()

    # epoch中的每一步
    def validation_step(self, batch, batch_idx):
        #这里是因为有时候抓不住测试epoch的start，所以在这判断一下，如果validation_epoch_start_time为0就说明是这个epoch的第一步，记录个时间
        if self.validation_epoch_start_time == 0:
             self.validation_epoch_start_time = time.time()
        images, labels = batch
        labels = labels.long()  # Ensure labels are Long type
        outputs = self(images)
        loss = nn.CrossEntropyLoss()(outputs, labels)
        preds = torch.argmax(outputs, dim=1)

        # Calculate and log metrics
        spec = self.spec(preds, labels)
        f1 = self.f1(preds, labels)
        prec = self.prec(preds, labels)
        rec = self.rec(preds, labels)
        acc = self.acc(preds, labels)

        self.log('val_loss', loss, prog_bar=True, logger=True)
        self.log('val_spec', spec, prog_bar=True, logger=True)
        self.log('val_f1', f1, prog_bar=True, logger=True)
        self.log('val_prec', prec, prog_bar=True, logger=True)
        self.log('val_rec', rec, prog_bar=True, logger=True)
        self.log('val_acc', acc, prog_bar=True, logger=True)

        return {'val_loss': loss}

    def validation_epoch_end(self, outputs):
        # 只要有开始时间就可以计算结束时间
        if self.validation_epoch_start_time != 0:
            epoch_time = time.time() - self.validation_epoch_start_time
            print(f"Epoch {self.current_epoch} Validation Time: {epoch_time:.2f}s")
            self.validation_epoch_start_time = 0
           
        
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        self.log('val_loss_epoch', avg_loss)
        # 记录数据，方便后面画图
        self.val_losses.append(avg_loss.item())
        val_acc = self.trainer.callback_metrics.get("val_acc")
        if val_acc: 
            self.val_accs.append(val_acc.item())

    def configure_optimizers(self):
        optimizer = madgrad.MADGRAD(filter(lambda p: p.requires_grad, self.parameters()), lr=self.learning_rate)
        return optimizer

    #绘图函数
    def plot_metrics(self, dpi=300):
        plt.figure(figsize=(12,5))
      
        # Loss曲线
        plt.subplot(121)
        plt.plot(self.train_losses, label='Train')
        plt.plot(self.val_losses, label='Val')
        plt.title('Loss Curve')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
      
        # Accuracy曲线
        plt.subplot(122)
        plt.plot(self.train_accs, label='Train')
        plt.plot(self.val_accs, label='Val')
        plt.title('Accuracy Curve')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
      
        # 保存和清理
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"metrics_{timestamp}.png"
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')  # 保存为高分辨率图片
        plt.close()  # 防止内存泄漏
        
        print(f"Metrics plot saved to {save_path}")
        


class MyModel_MultiTask(pl.LightningModule):
    def __init__(self, mlr=1e-5, free_epoch=80):
        super().__init__()
        self.model = CVFMultiTask(frozen=True)
        self.learning_rate = mlr
        self.BCEcriterion = nn.BCEWithLogitsLoss()
        self.free_epoch = free_epoch

        self.best_acc_view = 0.0
        self.best_acc_mi = 0.0
        self.best_acc_metrics_view = {}
        self.best_acc_metrics_mi = {}

    # 绘图数据存储，因为分不同任务，所以分开记录
        self.train_losses = []
        self.train_losses_view = []
        self.train_losses_mi = []
        self.train_accs_view = []
        self.train_accs_mi = []
        self.val_losses_view = []
        self.val_losses_mi = []
        self.val_accs_view = []
        self.val_accs_mi= []
        # 存训练和测试时间
        self.train_epoch_start_time = 0
        self.validation_epoch_start_time = 0

    def on_epoch_start(self):
        if self.current_epoch == self.free_epoch:
            # 第 50 个 epoch 开始时解冻心梗诊断相关模块
            self.model.unfreeze_mi_task()
            print("解冻心梗诊断模块的参数")

    def forward(self, x1, x2):
        # 返回三个logit值，分别是MI任务的logit和两个视图的logit
        logit_mi, logit_view1, logit_view2 = self.model(x1, x2)
        return logit_mi, logit_view1, logit_view2

    # epoch开始前存一个时间
    def on_train_epoch_start(self):
        self.train_epoch_start_time = time.time()
    
    # epoch结束后再记录一下时间，减最初的时间就是这一个epoch的时间
    def on_train_epoch_end(self):
        epoch_time = time.time() - self.train_epoch_start_time
        print(f"Epoch {self.current_epoch} Training Time: {epoch_time:.2f}s")
                # # 存一下这一个epoch的loss和acc，方便最后画图
        train_loss = self.trainer.callback_metrics.get("train_loss")
        train_loss_view = self.trainer.callback_metrics.get("train_loss_view")
        train_loss_mi =self.trainer.callback_metrics.get("train_loss_mi")
        train_acc_view = self.trainer.callback_metrics.get("train_acc_view")
        train_acc_mi = self.trainer.callback_metrics.get("train_acc_mi")
        
        if train_loss: 
            self.train_losses.append(train_loss.item())
        if train_loss_view: 
            self.train_losses_view.append(train_loss_view.item())
        if train_loss_mi: 
            self.train_losses_mi.append(train_loss_mi.item())
        if train_acc_view: 
            self.train_accs_view.append(train_acc_view.item())
        if train_acc_mi: 
            self.train_accs_mi.append(train_acc_mi.item())

    def training_step(self, batch, batch_idx):
        # for name, param in self.model.named_parameters():
        #     if param.grad is not None:
        #         print(f"gradient for {name}")
        # print(self.model.videoEncoder.echo_encoder.head[-1].requires_grad)
        (x1, x2), labels = batch
        view_labels = labels["View_label"]
        mi_labels = labels["MI_label"]

        # 前向传播
        logits_mi, logits_view1, logits_view2 = self(x1, x2)
        # 打印 logits 和标签的范围、形状

        # 计算切面分类任务的损失
        loss_view1 = self.BCEcriterion(logits_view1.squeeze(dim=1), view_labels[0].float())  # 对应第一个视频
        loss_view2 = self.BCEcriterion(logits_view2.squeeze(dim=1), view_labels[1].float())  # 对应第二个视频
        loss_view = (loss_view1 + loss_view2) / 2.0  # 对两个视频的切面分类任务的损失取平均

        if self.current_epoch >= self.free_epoch:
            # 只有在80个epoch之后才计算MI诊断任务的损失
            loss_mi = self.BCEcriterion(logits_mi.squeeze(), mi_labels.float())
            loss = loss_view + 2 * loss_mi
        # 总损失为切面分类任务和MI检测任务的损失之和
        else:
            loss = loss_view

        # 计算切面分类任务的准确率（合并两个视频的预测结果）
        preds_view1 = (torch.sigmoid(logits_view1) > 0.5).int()
        preds_view2 = (torch.sigmoid(logits_view2) > 0.5).int()
        all_preds_view = torch.cat([preds_view1, preds_view2], dim=0)  # 合并两个视频的预测
        all_labels_view = torch.cat([view_labels[0], view_labels[1]], dim=0)  # 合并两个视频的标签
        all_preds_view = all_preds_view.squeeze(dim=1)

        # print(all_preds_view)
        # print(all_labels_view)
        # 计算切面分类任务的准确率
        acc_view = torchmetrics.Accuracy("binary")(all_preds_view.cpu(), all_labels_view.cpu())

        # 计算MI诊断任务的准确率（仅在epoch >= 50时计算）
        acc_mi = torch.tensor(0).float()
        if self.current_epoch >= self.free_epoch:
            preds_mi = torch.sigmoid(logits_mi) > 0.5
            preds_mi = preds_mi.squeeze(dim=1)
            acc_mi = torchmetrics.Accuracy("binary")(preds_mi.cpu(), mi_labels.cpu())

        # 记录训练过程中的各类指标
        self.log("train_loss", loss)
        self.log("train_loss_view", loss_view)
        if self.current_epoch >= self.free_epoch:
            self.log("train_loss_mi", loss_mi)
        self.log("train_acc_view", acc_view, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        if self.current_epoch >= self.free_epoch:
          self.log("train_acc_mi", acc_mi, on_step=False, on_epoch=True, prog_bar=True, logger=True)

        return loss

    # 测试epoch前记录一个时间
    def validation_epoch_start(self):
        self.validation_epoch_start_time = time.time()
        
    def validation_step(self, batch, batch_idx):
        #这里是因为有时候抓不住测试epoch的start，所以在这判断一下，如果validation_epoch_start_time为0就说明是这个epoch的第一步，记录个时间
        if self.validation_epoch_start_time == 0:
             self.validation_epoch_start_time = time.time()
            
        (x1, x2), labels = batch
        view_labels = labels["View_label"]
        mi_labels = labels["MI_label"]

        # 前向传播
        logits_mi, logits_view1, logits_view2 = self(x1, x2)

        # 计算损失
        loss_view1 = self.BCEcriterion(logits_view1.squeeze(), view_labels[0].float())  # 对应第一个视频
        loss_view2 = self.BCEcriterion(logits_view2.squeeze(), view_labels[1].float())  # 对应第二个视频
        loss_mi = self.BCEcriterion(logits_mi.squeeze(), mi_labels.float())

        preds_view1 = torch.sigmoid(logits_view1)
        preds_view2 = torch.sigmoid(logits_view2)
        preds_mi = torch.sigmoid(logits_mi)

        return {
            "preds_view1": preds_view1,
            "true_view1": view_labels[0],
            "loss_view1": loss_view1,
            "preds_view2": preds_view2,
            "true_view2": view_labels[1],
            "loss_view2": loss_view2,
            "preds_mi": preds_mi,
            "true_mi": mi_labels,
            "loss_mi": loss_mi,
        }

    def validation_epoch_end(self, validation_step_outputs):
        preds_view1 = []
        true_view1 = []
        preds_view2 = []
        true_view2 = []
        preds_mi = []
        true_mi = []
        losses_view = []
        losses_mi = []

        # 汇总所有batch的输出
        for output in validation_step_outputs:
            preds_view1.append(output["preds_view1"])
            true_view1.append(output["true_view1"])
            preds_view2.append(output["preds_view2"])
            true_view2.append(output["true_view2"])
            preds_mi.append(output["preds_mi"])
            true_mi.append(output["true_mi"])
            losses_view.append(output["loss_view1"] + output["loss_view2"])  # 汇总切面分类任务损失
            losses_mi.append(output["loss_mi"])

        # 合并结果
        preds_view1 = torch.cat(preds_view1).cpu()
        true_view1 = torch.cat(true_view1).cpu()
        preds_view2 = torch.cat(preds_view2).cpu()
        true_view2 = torch.cat(true_view2).cpu()
        preds_mi = torch.cat(preds_mi).cpu()
        true_mi = torch.cat(true_mi).cpu()

        val_loss_view = torch.stack(losses_view).mean()
        val_loss_mi = torch.stack(losses_mi).mean()

        # 合并视图预测和标签
        all_preds_view = torch.cat([preds_view1, preds_view2], dim=0)
        all_labels_view = torch.cat([true_view1, true_view2], dim=0)


        # print("label:",all_labels_view)

        # 计算切面分类任务的准确率和AUC
        preds_view_binary = (all_preds_view > 0.5).int()
        preds_view_binary = preds_view_binary.squeeze(dim=1)
        # print("pred:",preds_view_binary)

        acc_view = torchmetrics.Accuracy("binary")(preds_view_binary, all_labels_view)
        prec_view = torchmetrics.Precision("binary")(preds_view_binary, all_labels_view)
        spec_view = torchmetrics.Specificity("binary")(preds_view_binary, all_labels_view)
        rec_view = torchmetrics.Recall("binary")(preds_view_binary, all_labels_view)
        f1_view = torchmetrics.F1Score("binary")(preds_view_binary, all_labels_view)
        auc_view = torchmetrics.AUROC("binary")(all_preds_view, all_labels_view)

        # 计算MI检测任务的准确率和AUC
        preds_mi_binary = (preds_mi > 0.5).int()
        preds_mi_binary = preds_mi_binary.squeeze(dim=1)
        acc_mi = torchmetrics.Accuracy("binary")(preds_mi_binary, true_mi)
        prec_mi = torchmetrics.Precision("binary")(preds_mi_binary, true_mi)
        spec_mi = torchmetrics.Specificity("binary")(preds_mi_binary, true_mi)
        rec_mi = torchmetrics.Recall("binary")(preds_mi_binary, true_mi)
        f1_mi = torchmetrics.F1Score("binary")(preds_mi_binary, true_mi)
        auc_mi = torchmetrics.AUROC("binary")(preds_mi, true_mi)

        # 打印和记录验证指标
        self.log("val_loss_view", val_loss_view, prog_bar=True, logger=True)
        if self.current_epoch >= self.free_epoch:
            self.log("val_loss_mi", val_loss_mi, prog_bar=True, logger=True)
        self.log("val_acc_view", acc_view, prog_bar=True, logger=True)
        self.log("val_prec_view", prec_view, prog_bar=True, logger=True)
        self.log("val_spec_view", spec_view, prog_bar=True, logger=True)
        self.log("val_rec_view", rec_view, prog_bar=True, logger=True)
        self.log("val_f1_view", f1_view, prog_bar=True, logger=True)
        self.log("val_auc_view", auc_view, prog_bar=True, logger=True)
        if self.current_epoch >= self.free_epoch:
            self.log("val_acc_mi", acc_mi, prog_bar=True, logger=True)
            self.log("val_prec_mi", prec_mi, prog_bar=True, logger=True)
            self.log("val_spec_mi", spec_mi, prog_bar=True, logger=True)
            self.log("val_rec_mi", rec_mi, prog_bar=True, logger=True)
            self.log("val_f1_mi", f1_mi, prog_bar=True, logger=True)
            self.log("val_auc_mi", auc_mi, prog_bar=True, logger=True)

        # 更新最佳 AUC 指标
        if acc_view >= self.best_acc_view and self.current_epoch > 80:
            self.best_acc_view = acc_view
            self.best_acc_metrics_view = {
                "val_acc_view": acc_view,
                "val_prec_view": prec_view,
                "val_spec_view": spec_view,
                "val_rec_view": rec_view,
                "val_f1_view": f1_view,
                "val_auc_view": auc_view
            }

        if self.current_epoch >= self.free_epoch:
            if acc_mi > self.best_acc_mi and self.current_epoch > self.free_epoch + 20:
                self.best_acc_mi = acc_mi
                self.best_acc_metrics_mi = {
                    "val_acc_mi": acc_mi,
                    "val_prec_mi": prec_mi,
                    "val_spec_mi": spec_mi,
                    "val_rec_mi": rec_mi,
                    "val_f1_mi": f1_mi,
                    "val_auc_mi": auc_mi
                }

        # 只要有开始时间就可以计算结束时间
        if self.validation_epoch_start_time != 0:
            epoch_time = time.time() - self.validation_epoch_start_time
            print(f"Epoch {self.current_epoch} Validation Time: {epoch_time:.2f}s")
            self.validation_epoch_start_time = 0
           
        # 记录数据，方便后面画图
        self.val_losses_view.append(val_loss_view.item())
        # 这里是为了让数据一样长，因为free_epoch之前没有MI任务，只有View任务
        if self.current_epoch >= self.free_epoch:
            self.val_losses_mi.append(val_loss_mi.item())
        else:
            self.val_losses_mi.append(0.0)  # 保持长度一致
      
        self.val_accs_view.append(acc_view.item())
        if self.current_epoch >= self.free_epoch:
            self.val_accs_mi.append(acc_mi.item())
            
    def configure_optimizers(self):
        optimizer = madgrad.MADGRAD(filter(lambda p: p.requires_grad, self.parameters()), lr=self.learning_rate)
        return optimizer

    #绘图函数
    def plot_metrics(self, dpi=300):
        plt.figure(figsize=(12,5))
      
        # Loss曲线
        # train的view、mi+验证的view、mi
        plt.subplot(121)
        plt.plot(self.train_losses_view, label='T_View')
        plt.plot(self.train_losses_mi, label='T_MI')
        plt.plot(self.val_losses_view, label='V_View')
        plt.plot(self.val_losses_mi, label='V_MI')
        plt.title('Loss Curve')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
      
        # Accuracy曲线
        # 和loss一样，分开列
        plt.subplot(122)
        plt.plot(self.train_accs_view, label='T_View')
        plt.plot(self.train_accs_mi, label='T_MI')
        plt.plot(self.val_accs_view, label='V_View')
        plt.plot(self.val_accs_mi, label='V_MI')
        plt.title('Accuracy Curve')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
      
        # 保存和清理
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"metrics_{timestamp}.png"
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')  # 保存为高分辨率图片
        plt.close()  # 防止内存泄漏
        
        print(f"Metrics plot saved to {save_path}")


