# -*- coding: utf-8 -*-
import numpy as np
import cv2.cv2 as cv2
import json


def tag2json(tagpath,
             tagname,
             pngpath,
             pngname,
             save=False,
             save_jsonpath=None,
             save_jsonname=None,
             save_pngpath=None,
             save_pngname=None):
    '''
    tagpath: 标注路径
    tagname: 标注名称
    pngpath：图片路径
    pngname：图片名称
    save：是否保存
    save_jsonpath: 保存json路径
    save_jsonname：保存json文件名称
    save_pngpath：保存png路径
    save_pngname：保存png名称

    return: None
    '''

    img = cv2.imread(pngpath + '/' + pngname)
    start_x = 0
    start_y = 0
    chunks = []
    with open(tagpath + '/' + tagname, encoding='utf8') as f:
        tags = f.readlines()
    for line in tags:
        tag = line.strip().split(',')
        pos, text = tag[:8], tag[8:]
        # print(text)

        tmp_text = ""
        for t in text:
            tmp_text += t
        text = tmp_text
        # print(text)

        if text == "":
            img = img[int(eval(pos[1])):int(eval(pos[7])),
                      int(eval(pos[0])):int(eval(pos[6]))]
            start_x = eval(pos[0])
            start_y = eval(pos[1])
            # # Display cropped image
            # width = int(img.shape[1] / 2)
            # height = int(img.shape[0] / 2)
            # dim = (width, height)

            # # resize image
            # resized = cv2.resize(img, dim)

            # # save the image
            # cv2.imshow("Image", resized)
            # cv2.waitKey(0)

            if save is True:
                assert save_pngpath is not None, 'save_pngpath is empty'
                cv2.imwrite(save_pngpath + '/' + save_pngname, img)
        else:
            tmp = {}
            pos_need = [
                eval(pos[0]) - start_x,
                eval(pos[6]) - start_x,
                eval(pos[1]) - start_y,
                eval(pos[7]) - start_y
            ]
            tmp["pos"] = pos_need
            tmp["text"] = text
            chunks.append(tmp)

    data = {}
    data["chunks"] = chunks
    # print(data)
    with open(save_jsonpath + '/' + save_jsonname, 'w',
              encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)  # 缩进两个字符输出


if __name__ == "__main__":
    tag2json(".",
             "tag.txt",
             ".",
             "tag.png",
             save=True,
             save_jsonpath=".",
             save_jsonname="result__.json",
             save_pngpath=".",
             save_pngname="result__.png")
