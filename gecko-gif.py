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

def sph2cart(sph: np.ndarray):
    # the last dimension of `sph` is expected to be in format [r, theta, phi]
    sph = np.array(sph)
    r     = sph[..., 0]
    theta = sph[..., 1]
    phi   = sph[..., 2]

    cart = np.zeros(np.shape(sph))
    cart[..., 0] = r * np.cos(phi) * np.sin(theta)
    cart[..., 1] = r * np.sin(phi) * np.sin(theta)
    cart[..., 2] = r * np.cos(theta)

    return cart

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

# TODO we spend too much time near the switching points and not enough time near
# the midpoint of each section
if _write_to_file:
    os.system('rm frames/*')
radius = 1
while True:
    phi = 0
    for theta in np.linspace(0, pi/2, 30, endpoint=False):
        im = mask * np.reshape(sph2cart([radius, theta, phi]), (1, 1, 3))
        if _write_to_file:
            cv.imwrite(_frame_path_prefix + 'A' + str(theta) + '.png', 255*im)
        else: update_window(im)
    theta = pi/2
    for phi in np.linspace(0, pi/2, 30, endpoint=False):
        im = mask * np.reshape(sph2cart([radius, theta, phi]), (1, 1, 3))
        if _write_to_file:
            cv.imwrite(_frame_path_prefix + 'B' + str(phi) + '.png', 255*im)
        else: update_window(im)
    phi = pi/2
    for theta in np.linspace(pi/2, 0, 30, endpoint=False):
        im = mask * np.reshape(sph2cart([radius, theta, phi]), (1, 1, 3))
        if _write_to_file:
            cv.imwrite(_frame_path_prefix + 'C' + str(pi - theta) + '.png',
                       255*im)
        else: update_window(im)
    
    if _write_to_file: break

if _write_to_file:
    os.system('convert frames/*.png -set delay 10 frames/HECKIN-GECKIN.gif')