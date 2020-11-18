# -*- coding: utf-8 -*-
import numpy as np
import os
import cv2.cv2 as cv2
from numpy import float32
from cnocr import CnOcr
import json
from pathlib import Path


def power1to2(pngpath, img_names, coordinates, savepath):
    '''
    pathpath: 图片路径
    img_names: 图片名称
    coordinate：坐标（png2location中的results）
    
    return: None
    savepath下会同时保存chunk、img和draw_img三个文件夹
    '''
    length = len(img_names)
    if Path(savepath + '/chunk').is_dir() is False:
        os.mkdir(savepath + '/chunk')
    if Path(savepath + '/img').is_dir() is False:
        os.mkdir(savepath + '/img')
    if Path(savepath + '/draw_img').is_dir() is False:
        os.mkdir(savepath + '/draw_img')
    s = 0

    for k in range(length):
        img_name = img_names[k]
        coordinate = coordinates[k]
        img = cv2.imread(pngpath + "/" + img_name)
        # Draw rectangle
        for i in coordinate[0]:
            if i[4] > 0.7:
                cv2.rectangle(img, (int(i[0]), int(i[1])),
                              (int(i[2]), int(i[3])), (50, 205, 50), 4)
                img[int(i[0]):int(i[2]), int(i[1]):int(i[3])]
        for i in coordinate[1]:
            if i[4] > 0.7:
                cv2.rectangle(img, (int(i[0]), int(i[1])),
                              (int(i[2]), int(i[3])), (193, 210, 240), 4)
        for i in coordinate[2]:
            if i[4] > 0.7:
                cv2.rectangle(img, (int(i[0]), int(i[1])),
                              (int(i[2]), int(i[3])), (254, 67, 101), 4)

        cv2.imwrite(savepath + '/draw_img/' + img_name, img)

        # Cut img
        j = 0
        for i in coordinate[2]:
            if i[4] > 0.7:
                cropped = img[int(i[1]):int(i[3]),
                              int(i[0]):int(i[2])]  # 裁剪坐标为[y0:y1, x0:x1]
                # print(cropped)
                start_x = int(i[0])
                start_y = int(i[1])
                cv2.imwrite(savepath + '/img/' + str(j) + img_name, cropped)
                # print(img_name)
                j += 1

        # Json
        data = {}
        data['chunk'] = []

        for i in coordinate[1]:
            if i[4] > 0.7:
                cropped = img[int(i[1]):int(i[3]),
                              int(i[0]):int(i[2])]  # 裁剪坐标为[y0:y1, x0:x1]
                # print(cropped)
                ocr = CnOcr(name='instance' + str(s))
                s += 1
                # print(ocr.ocr(cropped))
                text = ""
                res_ocrs = ocr.ocr(cropped)
                if res_ocrs != []:
                    for res_ocr in res_ocrs:
                        for res in res_ocr:
                            text = text + res

                # text = "".join(ocr.ocr(cropped)[0])
                tmp = {}
                tmp["pos"] = [
                    i[0] - start_x, i[2] - start_x, i[1] - start_y,
                    i[3] - start_y
                ]
                for x in range(4):
                    if tmp["pos"][x] < 0:
                        tmp["pos"][x] = 0

                tmp["text"] = text
                data['chunk'].append(tmp)

        with open(savepath + '/chunk/' + img_name + ".json",
                  'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False,
                      indent=2)  # 缩进两个字符输出
