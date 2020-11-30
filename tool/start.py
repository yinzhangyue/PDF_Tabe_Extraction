# -*- coding: utf-8 -*-
from code.pdf2png import pdf2png
from code.power1to2 import power1to2
from mmdetection.png2location import png2location

if __name__ == "__main__":
    img_cvs, img_names = pdf2png(".",
                                 "aapl-20200926.pdf",
                                 save=True,
                                 savepath="./output/pict")
    results = png2location("./output/pict", img_names)
    power1to2("./output/pict", img_names, results, "./output")
