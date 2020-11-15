# -*- coding: utf-8 -*-
import numpy as np
import cv2.cv2 as cv2


def tag2view(tagpath,
             tagname,
             pngpath,
             pngname,
             save=False,
             savepath=None,
             savename=None):
    '''
    tagpath: 标注路径
    tagname: 标注名称
    pngpath：图片路径
    pngname：图片名称
    save：是否保存
    savepath: 保存路径
    savename：保存文件名称

    return: None
    '''
    img = cv2.imread(pngpath + '/' + pngname)

    with open(tagpath + '/' + tagname, encoding='utf8') as f:
        tags = f.readlines()
    for line in tags:
        tag = line.strip().split(',')
        pos, text = tag[:8], tag[8:]
        if text == ['']:
            cv2.rectangle(img, (int(eval(pos[0])), int(eval(pos[1]))),
                          (int(eval(pos[6])), int(eval(pos[7]))),
                          (254, 67, 101), 4)
        else:
            cv2.rectangle(img, (int(eval(pos[0])), int(eval(pos[1]))),
                          (int(eval(pos[6])), int(eval(pos[7]))),
                          (50, 205, 50), 4)
    # Display cropped image
    width = int(img.shape[1] / 3)
    height = int(img.shape[0] / 3)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim)

    # save the image
    cv2.imshow("Image", resized)
    cv2.waitKey(0)
    if save is True:
        assert savepath is not None, 'savepath is empty'
        assert savename is not None, 'savename is not given'
        cv2.imwrite(savepath + '/' + savename, img)


if __name__ == "__main__":
    tag2view(".",
             "tag.txt",
             ".",
             "tag.png",
             save=True,
             savepath=".",
             savename="result_.png")
