# -*- coding: utf-8 -*-
import numpy as np
import cv2.cv2 as cv2
from numpy import float32

if __name__ == "__main__":
    # Read image
    img = cv2.imread("./1/demo.png")
    a = np.array([[218.06601, 63.345993, 499.1235, 359.6285, 0.99998415]],
                 dtype=float32)
    b = np.array([[19.75746, 396.25815, 289.44995, 466.0727, 0.87934923]],
                 dtype=float32)
    # Draw rectangle
    j = 0
    for i in a:
        if i[4] > 0.7:
            cv2.rectangle(img, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])),
                          (50, 205, 50), 4)
            # cut = img[int(i[0]):int(i[2]), int(i[1]):int(i[3])]
            # cv2.imwrite('./pic/' + str(j) + '.png', cut)
            # j += 1
    # for i in b:
    #     if i[4] > 0.7:
    #         cv2.rectangle(img, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])),
    #                       (254, 67, 101), 4)
    # Display cropped image
    width = int(img.shape[1] / 4)
    height = int(img.shape[0] / 4)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim)

    # save the image
    cv2.imshow("Image", resized)
    cv2.waitKey(0)

    cv2.imwrite('./demo_.png', img)
