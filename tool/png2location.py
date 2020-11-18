from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
import torch
import numpy as np
from numpy import float32

# print("Successfullt load")
# print(torch.cuda.is_available())

# Load model
config_file = '/remote-home/zyyin/Experiment/pdfTableReader/mmdetection/CascadeTabNet/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py'
checkpoint_file = '/remote-home/zyyin/Experiment/pdfTableReader/mmdetection/CascadeTabNet/epoch_36.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')


def png2location(pngpath, img_names):
    '''
    pathpath: 图片路径
    img_names: 图片名称
    
    return: 
    results：list 包含result[0][0] 有表格线框 
                      result[0][1] 无表格线单元格
                      result[0][2] 无表格线框
    '''
    results = []
    for img_name in img_names:
        img = pngpath + "/" + img_name
        result = inference_detector(model, img)
        results.append([result[0][0], result[0][1], result[0][2]])

    return results
