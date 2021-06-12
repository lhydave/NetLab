import argparse
from time import time
import numpy as np
import cv2


def runtime(func):
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        print(f'Function [{func.__name__}] runtime: {time()-start:.2f}')
        return res

    return wrapper


@runtime
def video_import(filename: str, numfrm: int = 0) -> list[np.array]:
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    dims = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(fps, dims, frames)
    F = []
    num = 0
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    F = video_import(args.filename)
    print(len(F))
