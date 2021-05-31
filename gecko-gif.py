#!/bin/python3

import cv2 as cv
import numpy as np
from numpy import pi
import os

_win_name = 'HECKO GECKO'
_win_wait_interval_ms = 10
_frame_path_prefix = 'frames/HECKO-GECKO-'
_discord_size = (120, 120)
_resize_for_discord = False
_write_to_file = False

def imshow(window_name: str, im: np.ndarray):
    if _resize_for_discord:
        sz = (1000, 1000)
    else:
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
if _resize_for_discord:
    mask = mask[:, :mask.shape[0]]
    mask = cv.resize(mask*1.0, _discord_size, interpolation=cv.INTER_AREA)
# mask[...] = 1 # DEBUG

ratio = mask.shape[1]/mask.shape[0]
eye_pos = (-0.23, 0.03) if _resize_for_discord else (-0.23, -0.2)
x = np.linspace(-ratio - eye_pos[1], ratio - eye_pos[1], mask.shape[1])
y = np.linspace(-1 - eye_pos[0], 1 - eye_pos[0], mask.shape[0])
r = np.sqrt(
        np.sum(
            np.meshgrid(x**2, y**2),
            axis=0
        )
    )
pos_phase_shift = pi*r

L = 70
radius = 120

if _write_to_file: os.system('rm frames/*')
im = np.zeros((mask.shape[0], mask.shape[1], 3))
while True:
    for theta in np.linspace(0, 2*pi, 100):
        a = radius*np.cos(theta - pos_phase_shift)
        b = radius*np.sin(theta - pos_phase_shift)
        im[..., 0] = L * mask
        im[..., 1] = a * mask
        im[..., 2] = b * mask
        im = cv.cvtColor(im.astype('float32'), cv.COLOR_Lab2BGR)
        if _write_to_file:
            cv.imwrite(_frame_path_prefix + str(theta) + '.png', 255*im)
        else:
            update_window(im)
    
    if _write_to_file: break

if _write_to_file:
    gif_path = 'saved/HECKIN-GECKIN-L' + str(L) + 'r' + str(radius) + '-eye'
    if _resize_for_discord:
        gif_path += '-discord'
    gif_path += '.gif'
    os.system('convert frames/*.png -set delay 10 ' + gif_path)