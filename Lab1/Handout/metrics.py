from __future__ import division
import numpy as np
from skimage import morphology
from utils import *


def blur_fft(img: np.array, size: int = 60) -> float:
    h, w = img.shape
    ci, cj = h // 2, w // 2
    fft = np.fft.fft2(img)
    shift = np.fft.fftshift(fft)
    shift[ci - size:ci + size, cj - size:cj + size] = 0
    shift = np.fft.ifftshift(shift)
    recon = np.fft.ifft2(shift)
    magnitude = 20 * np.log(np.abs(recon))
    return np.mean(magnitude)


@runtime
def blur_level(seq: list[np.array]) -> list[float]:
    blur = []
    for frame in seq:
        blur.append(blur_fft(frame))
    return blur


@runtime
def freeze_detect(seq: list[np.array]) -> list[int]:
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
def noise_level(seq: list[np.array],
                thres: int = 40,
                size: int = 8) -> list[float]:
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
