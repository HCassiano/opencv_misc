# import the necessary packages
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Do stuff with images')
parser.add_argument('image', metavar='image', type=str,
                    help='image input')

args = parser.parse_args()
img = cv2.imread(args.image,0)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


