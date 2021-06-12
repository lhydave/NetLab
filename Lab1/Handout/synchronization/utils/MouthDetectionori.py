import cv2 as cv
from facenet_pytorch import MTCNN
import numpy as np
from PIL import Image


def detect_mouth(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    mouth_cascade = cv.CascadeClassifier(r'./haarcascade_mcs_mouth.xml')
    mouth = mouth_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in mouth:
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv.imshow('img', img)
    cv.waitKey()


def detect_face(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    face_cascade = cv.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5)
    for (x, y, w, h) in face:
        print(x, y, w, h)
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv.imshow('img', img)
    cv.waitKey()


def detect_face_byMTCNN(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    bboxs, prob = mtcnn.detect(img)
    return bboxs


mtcnn = MTCNN(image_size=224, margin=1)
