from PIL import Image
import pytesseract
import argparse
import cv2
import os


def OCR_dat(filepath):
    # load the example image and convert it to grayscale
    #image = cv2.imread(filepath)
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(Image.open(filepath))
    return text
