#coding=utf-8

import mxnet as mx
import json
from cnocr import CnOcr
# ocr = CnOcr()
# img_fp = './1.png'
# img = mx.image.imread(img_fp, 1)
# res = ocr.ocr(img)
# print("Predicted Chars:", "".join(res[0]))

from cnstd import CnStd

std = CnStd()
cn_ocr = CnOcr()


def ocr(pngpath, pngname, save=False, save_jsonpath=None, save_jsonname=None):
    '''
    pngpath：图片路径
    pngname：图片名称
    save：是否保存
    save_jsonpath: 保存json路径
    save_jsonname：保存json文件名称
    save_pngpath：保存png路径
    save_pngname：保存png名称

    return: None
    '''
    box_info_list = std.detect(pngpath + '/' + pngname)

    data = {}
    data["chunks"] = []
    for box_info in box_info_list:
        tmp = {}
        cropped_img = box_info['cropped_img']  # 检测出的文本框
        tmp_pos = [
            float(box_info['box'][0][0]),
            float(box_info['box'][1][0]),
            float(box_info['box'][0][1]),
            float(box_info['box'][2][1])
        ]
        tmp_text = ''.join(cn_ocr.ocr_for_single_line(cropped_img))
        tmp["pos"] = tmp_pos
        tmp["text"] = tmp_text

        ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
        data["chunks"].append(tmp)
    print(data)
    if save is True:
        # print(data)
        with open(save_jsonpath + '/' + save_jsonname, 'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False,
                      indent=2)  # 缩进两个字符输出
    else:
        print(json.dump(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    ocr(pngpath=".",
        pngname="2.png",
        save=True,
        save_jsonpath=".",
        save_jsonname="result.json")