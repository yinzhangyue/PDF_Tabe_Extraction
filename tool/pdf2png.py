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
    
    return: list 包含pdf转换后每张图片的矩阵形式
    '''
    doc = fitz.open(filepath + '/' + filename)
    img_cvs = []
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
        cv2.imshow("Image", cv2.resize(img_cv, (540, 800)))
        cv2.waitKey(0)
        img_cvs.append(img_cv)
        if save is True:
            assert savepath is not None, 'savepath is empty'
            pm.writePNG(savepath + '/%s.png' % pg)
    return img_cvs


# if __name__ == "__main__":
#     pdf2png(".", "1.pdf")