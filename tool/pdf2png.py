# -*- coding: utf-8 -*-
import fitz
import numpy as np
import cv2.cv2 as cv2


#  pip install PyMuPDF
#  打开PDF文件，生成一个对象
def pdf2png(filepath, filename, save=False, savepath=None):
    '''
    filepath: 文件路径
    filename: 文件名称
    save：是否保存
    savepath: 保存路径
    
    return: 
    img_cvs：list 包含pdf转换后每张图片的矩阵形式
    img_names：list 包含每张图片的名称
    '''
    doc = fitz.open(filepath + '/' + filename)
    img_cvs = []
    img_names = []
    for pg in range(doc.pageCount):
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为4，这将为我们生成分辨率提高16倍的图像。
        zoom_x = 4.0
        zoom_y = 4.0
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        # print(pm)

        getpngdata = pm.getImageData(output="png")

        # 解码为 np.uint8
        image_array = np.frombuffer(getpngdata, dtype=np.uint8)
        img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)

        # 显示图片
        # cv2.imshow("Image", cv2.resize(img_cv, (540, 800)))
        # cv2.waitKey(0)

        img_cv = cv2.resize(img_cv, (2100, 2970))
        img_cvs.append(img_cv)
        if save is True:
            assert savepath is not None, 'savepath is empty'
            # pm.writePNG(savepath + '/%s.png' % pg)
            cv2.imwrite(savepath + '/%s.png' % pg, img_cv)
            img_names.append('%s.png' % pg)
    return img_cvs, img_names


# if __name__ == "__main__":
#     pdf2png(".", "aapl-20200926.pdf", save=True, savepath="./pict")
