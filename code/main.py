# -*- coding: utf-8 -*-
import fitz
import numpy as np
import cv2.cv2 as cv2
from border import border
from mmdet.apis import inference_detector, show_result, init_detector
from Functions.blessFunc import borderless
import lxml.etree as etree
import glob
import sys
import os
import chunk2xlsx


def pdf2png(filepath, filename, save=False, savepath=None):
    '''
    filepath: 文件路径
    filename: 文件名称
    save：是否保存
    savepath: 保存路径
    
    return: 
    pm.width：图片宽度
    pm.height：图片长度
    '''
    doc = fitz.open(filepath + '/' + filename)
    img_cvs = []
    img_names = []
    for pg in range(doc.pageCount):
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高4倍的图像。
        zoom_x = 2.0
        zoom_y = 2.0
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        # print(pm.width, pm.height)
        if save is True:
            assert savepath is not None, 'savepath is empty'
            # pm.writePNG(savepath + '/%s.png' % pg)
            pm.writePNG(savepath + '/%s.png' % (pg + 1))  #将图片写入指定的文件夹内
    return pm.width, pm.height


# 单元格合并
def blockMerge(infoList):
    res = horizontalBlockMerge(infoList)
    res = verticalBlockMerge(res)
    return res


# 水平单元格合并
def horizontalBlockMerge(infoList):
    blockMap = {}
    for cell in infoList:
        key = (cell[5], cell[6])
        if key not in blockMap:
            blockMap[key] = [cell]
        else:
            blockMap[key].append(cell)
    res = []
    for key in blockMap:
        if len(blockMap[key]) == 1:
            res.append(blockMap[key][0])
        elif len(blockMap[key]) > 1:
            mergeCell = [
                min(blockMap[key], key=lambda x: x[0])[0],
                min(blockMap[key], key=lambda x: x[1])[1],
                max(blockMap[key], key=lambda x: x[2])[2],
                max(blockMap[key], key=lambda x: x[3])[3]
            ]
            content = ''
            for subCell in blockMap[key]:
                content += subCell[4] + ' '
            mergeCell.append(content)
            mergeCell.extend([key[0], key[1], 0])
            res.append(mergeCell)
    return res


# 垂直单元格合并
def verticalBlockMerge(infoList):
    blockMap = {}
    for cell in infoList:
        key = cell[5]
        if key not in blockMap:
            blockMap[key] = [cell]
        else:
            blockMap[key].append(cell)
    res = []
    for key in blockMap:
        lineData = blockMap[key]
        if len(lineData) == 1:
            res.append(lineData[0])
        elif len(lineData) > 1:
            lineData = sorted(lineData, key=lambda x: x[6])
            # first = lineData[0]
            mergeCell = lineData[0]
            for i in range(1, len(lineData)):
                if not chunk2xlsx.ifSameRow(mergeCell, lineData[i]) \
                        and chunk2xlsx.ifSameCol(mergeCell, lineData[i]):
                    mergeCell[4] += lineData[i][4]
                    mergeCell[2], mergeCell[3] = max(lineData[i][2], mergeCell[2]),\
                                                 max(lineData[i][3], mergeCell[3])
                    # mergeCell[1], mergeCell[3] = first[1], first[3]
                else:
                    res.append(mergeCell)
                    mergeCell = lineData[i]
            # mergeCell[1], mergeCell[3] = first[1], first[3]
            res.append(mergeCell)
        else:
            pass
    return res


def loc2sxlsx(pdfpath, xlsxpath, xlsxname, num, png_width, png_height, table,
              image):
    '''
    pdfpath: pdf路径
    xlsxpath：保存xlsx的位置
    xlsxname：保存xlsx的名称
    num: 页码
    png_width：图片宽度
    png_height: 图片长度
    table：表格位置
    image: 图片

    return: None
    '''
    doc = fitz.open(pdfpath)
    page = doc[num]
    pm = page.getPixmap()
    delta = 6
    x1 = table[0] / png_width * pm.width - delta
    y1 = table[1] / png_height * pm.height - delta
    x2 = table[2] / png_width * pm.width + delta
    y2 = table[3] / png_height * pm.height + delta
    info_list = page.getTextPage().extractWORDS()
    need_list = []
    for info in info_list:
        if info[0] >= x1 and info[1] >= y1 and info[2] <= x2 and info[3] <= y2:
            info_tmp = list(info)
            if info_tmp[2] - info_tmp[0] < 35:
                info_tmp[0] -= 6
                info_tmp[2] += 6
            need_list.append(info_tmp)

    mergedCell = blockMerge(need_list)
    given_list = []
    for cell in mergedCell:
        given_list.append(chunk2xlsx.dataInput(cell))
    chunks = chunk2xlsx.chunk2Structure(given_list)
    chunk2xlsx.transformStructureToTable(chunks, xlsxname, savePath=xlsxpath)
    newImage = chunk2xlsx.generatePNG(image, chunks, table)
    return newImage, chunks


def find_table(location, table_width=1616 / 2):
    table_loc_tmp = []
    for ind, loc in enumerate(location):
        if loc[4] > 0.85:
            if loc[2] - loc[0] >= table_width:
                table_loc_tmp.append([loc[0], loc[1], loc[2], loc[3]])

    table_loc = []
    for (x1, y1, x2, y2) in table_loc_tmp:
        for ind, loc in enumerate(location):
            if loc[4] > 0.85:
                if x1 <= loc[0] and y1 <= loc[1] and x2 >= loc[
                        2] and y2 >= loc[3]:
                    continue
                if x1 > loc[0] and y1 <= loc[1] and x2 >= loc[2] and y2 >= loc[
                        3]:
                    x1 = loc[0]
                if x1 <= loc[0] and y1 <= loc[1] and x2 < loc[2] and y2 >= loc[
                        3]:
                    x2 = loc[2]
        y1 -= 3
        y2 += 3
        table_loc.append((int(x1), int(y1), int(x2), int(y2)))
    # print(table_loc)
    return table_loc


def solve(filepath, image_path, xlsxpath, chunkspath, pdfpath, png_width,
          png_height):
    ############ To Do ############
    # image_path = './Examples/demo.png'
    # xmlPath = './Examples/'

    config_fname = "./config_table.py"
    checkpoint_path = "./"
    epoch = 'epoch_36.pth'
    image_path = filepath + image_path
    xlsxpath = filepath + xlsxpath
    pdfpath = filepath + pdfpath
    chunkspath = filepath + chunkspath
    ##############################

    model = init_detector(config_fname, checkpoint_path + epoch)

    # List of images in the image_path
    imgs = glob.glob(image_path)
    info = {}
    for index, i in enumerate(imgs):
        i_name = i.split('/')[-1][:-4]
        print('###{}###'.format(i_name))
        result = inference_detector(model, i)
        # print(result)

        table_loc = find_table(result[0])
        img = cv2.imread(i)
        xlsxnames = []
        for ind, (x1, y1, x2, y2) in enumerate(table_loc):
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (222,156,83), 2)
            xlsxname = i_name + chr(ord('a') + ind)
            img, chunks = loc2sxlsx(pdfpath=pdfpath,
                                    xlsxpath=xlsxpath,
                                    xlsxname=xlsxname,
                                    num=int(i_name) - 1,
                                    png_width=png_width,
                                    png_height=png_height,
                                    table=[x1, y1, x2, y2],
                                    image=img)
            xlsxnames.append(xlsxname)
            chunk2xlsx.saveChunks(chunks, chunkspath, xlsxname)
        cv2.imwrite(i, img)
        info[index] = xlsxnames
    return info


def png2pdf(image_path, output_path):
    doc = fitz.open()
    for img in sorted(glob.glob(image_path)):  # 读取图片，确保按文件名排序
        # print(img)
        imgdoc = fitz.open(img)  # 打开图片
        pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)  # 将当前页插入文档
    if os.path.exists(output_path):
        os.remove(output_path)
    doc.save(output_path)  # 保存pdf文件
    doc.close()


if __name__ == "__main__":
    filename = sys.argv[1]
    os.mkdir('./' + filename + '/img')
    os.mkdir('./' + filename + '/xlsx')
    os.mkdir('./' + filename + '/chunks')
    width, height = pdf2png('./' + filename,
                            filename + '.pdf',
                            True,
                            savepath='./' + filename + '/img')
    print("IMG Done.")
    # width, height = 1191, 1616
    info = solve(filepath='./' + filename,
                 image_path='/img/*.png',
                 xlsxpath='/xlsx/',
                 chunkspath='/chunks/',
                 pdfpath='/' + filename + '.pdf',
                 png_width=width,
                 png_height=height)
    print(info)
    png2pdf(image_path='./' + filename + '/img/*.png',
            output_path='./' + filename + '/' + filename + '_.pdf')
