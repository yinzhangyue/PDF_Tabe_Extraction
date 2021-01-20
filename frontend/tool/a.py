# -*- coding: utf-8 -*-
import numpy as np
import cv2.cv2 as cv2
from numpy import float32

if __name__ == "__main__":
    # Read image
    img = cv2.imread("./c73.png")
    a = np.array([[
        1458.4429931640625, 145.316650390625, 1554.5313720703125,
        176.924560546875, 1
    ]],
                 dtype=float32)
    b = np.array([[
        1734.0457763671875, 191.89208984375, 1829.681640625, 222.283935546875,
        1
    ]],
                 dtype=float32)
    # Draw rectangle
    j = 0
    for i in a:
        if i[4] > 0.85:
            cv2.rectangle(img, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])),
                          (50, 205, 50), 4)
            # cut = img[int(i[0]):int(i[2]), int(i[1]):int(i[3])]
            # cv2.imwrite('./pic/' + str(j) + '.png', cut)
            # j += 1
    for i in b:
        if i[4] > 0.85:
            cv2.rectangle(img, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])),
                          (254, 67, 101), 4)
    # Display cropped image
    width = int(img.shape[1] / 4)
    height = int(img.shape[0] / 4)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim)

    # save the image
    cv2.imshow("Image", resized)
    cv2.waitKey(0)

    cv2.imwrite('./c73_.png', img)
