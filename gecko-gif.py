#!/bin/python3

import cv2 as cv
import numpy as np
from numpy import pi
import os

_win_name = 'HECKO GECKO'
_win_wait_interval_ms = 10
_frame_path_prefix = 'frames/HECKO-GECKO-'
_resize_for_discord = False
_write_to_file = False

def imshow(window_name: str, im: np.ndarray):
    ratio = im.shape[0]/im.shape[1]
    width = 1000
    sz = (width, int(width*ratio))
    cv.imshow(window_name, cv.resize(im, sz))

def update_window(im: np.ndarray):
    imshow(_win_name, im)
    cv.waitKey(_win_wait_interval_ms)

im = cv.imread('gecko-recolored.jpg')
im = im/255.0
mask = np.linalg.norm(im, axis=2) > 0.3
mask = np.repeat(mask[..., np.newaxis], 3, axis=2)
if _resize_for_discord:
    mask = mask[:, :mask.shape[0], :]
    mask = cv.resize(mask*1.0, (120, 120), interpolation=cv.INTER_AREA)

y = np.linspace(0, pi, im.shape[1])

if _write_to_file:
    os.system('rm frames/*')
L = 70
radius = 120
while True:
    for theta in np.linspace(0, 2*pi, 150):
        a = radius*np.cos(theta)
        b = radius*np.sin(theta)
        im = mask * [L, a, b]
        im = cv.cvtColor(im.astype('float32'), cv.COLOR_Lab2BGR)
        if _write_to_file:
            cv.imwrite(_frame_path_prefix + str(theta) + '.png', 255*im)
        else:
            update_window(im)
    
    if _write_to_file: break

if _write_to_file:
    os.system('convert frames/*.png -set delay 10 frames/HECKIN-GECKIN.gif')