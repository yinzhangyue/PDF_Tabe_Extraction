from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
import torch

# print("Successfullt load")
# print(torch.cuda.is_available())

# Load model
config_file = './CascadeTabNet/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py'
checkpoint_file = './CascadeTabNet/epoch_36.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')

# Test a single image
# img = "./CascadeTabNet/Demo/demo.png"
img = "./CascadeTabNet/pict/6.png"
# Run Inference
result = inference_detector(model, img)

print(result[0])
print(type(result[0]))

print(result[0][0])
print(result[0][1])
print(result[0][2])
# Visualization results
# show_result_pyplot(img,
#                    result, ('Bordered', 'cell', 'Borderless'),
#                    score_thr=0.85)
