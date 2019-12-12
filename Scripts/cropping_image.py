import cv2
import numpy as np
import os

def cropping_image(path, output_path):
    for image in os.listdir(f'{path}'):
        img = cv2.imread(f'{path}/{image}')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = 255*(gray < 128).astype(np.uint8)
        coords = cv2.findNonZero(gray)
        x, y, w, h = cv2.boundingRect(coords)
        rect = img[y:y+h, x:x+w]
        cv2.imwrite(f'{output_path}/{image}Cropped.ppm', rect)