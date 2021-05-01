# -*- coding: utf-8 -*-
"""4 metrics (CPU).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TX1nI_greNKWttVUdltQ_QMSg5JfCOAa
"""

import os

from time import time
import numpy as np
import cv2
import sys

from skimage import morphology

def runtime(func):
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        print(f'Function [{func.__name__}] runtime: {time()-start:.2f}')
        return res

    return wrapper


@runtime
def video_import(filename: str, numfrm: int = 0,beginfrm: int = 0) -> list:
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    dims = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(fps, dims, frames)
    F = []
    num = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES,beginfrm)
    success, frame = cap.read()
    while success:
        num += 1
        F.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        if numfrm > 0 and num >= numfrm:
            break
        success, frame = cap.read()
    cap.release()
    print(f'Successfully import {len(F)} frames.')
    return F

@runtime
def freeze_detect(seq: list) -> list:
    m_image = 30
    f_cut = 0.02
    a = 2.5
    b = 1.25
    c = 0.1
    m_drop = 0.015
    N = len(seq)
    ti = []  # temporal information
    for t in range(1, N):
        diff = np.abs(seq[t] - seq[t - 1])
        diff[diff < m_image] = 0
        ti.append(np.mean(np.power(diff, 2)))
    # print(ti)
    ti_sort = ti.copy()
    ti_sort.sort()
    l = int(np.ceil(f_cut * (N - 1)))
    r = int(np.floor((1 - f_cut) * (N - 1)))
    ti_avg = np.mean(ti_sort[l:r + 1])
    dfact = max(a + b * np.log(ti_avg), c)
    drops = [1 if x <= dfact * m_drop else 0 for x in ti]
    return drops

@runtime
def noise_level(seq: list,
                thres: int = 40,
                size: int = 8) -> list:
    N = len(seq)
    noise = []
    for t in range(1, N):
        diff = np.abs(seq[t] - seq[t - 1])
        m1 = diff > thres
        m2 = morphology.remove_small_objects(m1, connectivity=2, min_size=size)
        m = np.logical_or(np.logical_not(m1), m2)
        diff[m] = 0
        noise.append(diff.mean())
    return noise

def one_clip(filename,numfrm,beginfrm):
    F = video_import(filename,numfrm,beginfrm)
    freeze=np.array(freeze_detect(F)).sum()
    noise=np.array(noise_level(F)).mean()
    return freeze,noise

def full_video(filename,numfrm):
    print(filename)
    cap = cv2.VideoCapture(filename)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    freeze=[]
    noise=[]
    for beginfrm in range(0,frames,numfrm):
        print(beginfrm,frames,numfrm)
        f,n=one_clip(filename,numfrm,beginfrm)
        freeze.append(f)
        noise.append(n)
    return freeze,noise

GAP=100
def freeze_noise(video,outfile_freeze,outfile_noise):
  freeze,noise=full_video(video,GAP)
  with open(outfile_freeze,'a') as f:
    f.write('freeze:\n')
    for i in freeze:
      f.write(str(i)+'\n')
  with open(outfile_noise,'a') as f:
    f.write('noise:\n')
    for i in noise:
      f.write(str(i)+'\n')

if __name__ =='__main__':
    freeze_noise(sys.argv[1],sys.argv[2],sys.argv[3])