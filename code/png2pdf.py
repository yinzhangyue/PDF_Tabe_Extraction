import glob
import fitz
import os


def png2pdf():
    doc = fitz.open()
    for img in sorted(glob.glob("./img/*")):  # 读取图片，确保按文件名排序
        # print(img)
        imgdoc = fitz.open(img)  # 打开图片
        pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)  # 将当前页插入文档
    if os.path.exists("allimages.pdf"):
        os.remove("allimages.pdf")
    doc.save("allimages.pdf")  # 保存pdf文件
    doc.close()


if __name__ == '__main__':
    png2pdf()
