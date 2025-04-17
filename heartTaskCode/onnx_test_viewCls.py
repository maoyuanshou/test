import onnxruntime
import torch
from datasets import Mydataset_Sichuan_ViewCls
from torch.utils.data import DataLoader

# 定义 ONNX 模型的路径
onnx_path = "./onnx/viewCls-model.onnx"

# 创建一个 ONNX Runtime 会话
session = onnxruntime.InferenceSession(onnx_path)

# 获取模型的输入名称
input_name = session.get_inputs()[0].name

# 加载数据集:先用四川省试下,也方便跑对比
test_dataset = Mydataset_Sichuan_ViewCls(r"/root/autodl-tmp/heartTaskCode/切面分类/test.txt")
test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False)

# 取一个样本进行推理
for data in test_dataloader:
    input_tensor = data  # 假设数据集中的样本可以直接作为输入
    if isinstance(input_tensor, tuple):
        input_tensor = input_tensor[0]  # 如果返回的是 (input, label) 形式，取输入部分
    input_tensor = input_tensor.numpy()

    # 运行推理
    outputs = session.run(None, {input_name: input_tensor})

    # 输出推理结果
    print("推理结果:", outputs)
    break  # 只进行一次推理，如果需要对所有样本推理，可去掉这一行