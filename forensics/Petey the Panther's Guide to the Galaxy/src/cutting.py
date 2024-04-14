import cv2
import numpy as np
import math

img = cv2.imread('small.png')

# 400 pieces is probably enough, but i can alter this if I wanna make it less brute-forceable
x, y, _ = img.shape
piece_width = x // 20
piece_height = y // 20

piece_num = 0
for i in range(0, x, piece_width):
    for j in range(0, y, piece_height):
        piece = img[i:min(i+piece_width, x), j:min(j+piece_height, y)]
        cv2.imwrite(f'piece_{piece_num}.png', piece)
        piece_num += 1
