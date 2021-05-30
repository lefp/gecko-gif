#!/bin/python3

import cv2 as cv
import numpy as np

a, b = np.meshgrid(np.linspace(-128, 127, 500), np.transpose(np.linspace(-128, 127, 500)))
a = np.array(a)
b = np.array(b)
L = 70*np.ones((500, 500, 1))
im = np.concatenate((L, a[..., np.newaxis], b[..., np.newaxis]), axis=2)
im = cv.cvtColor(im.astype('float32'), cv.COLOR_Lab2BGR)
cv.imshow('col', im)
cv.waitKey()