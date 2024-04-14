import cv2
import numpy as np
import glob
import math

pieces = sorted(glob.glob('piece_*.png'), key=lambda x: int(x.split('_')[1].split('.')[0]))

# Getting my original image sized up
num_pieces = len(pieces)
rows = cols = int(math.sqrt(num_pieces))
piece_img = cv2.imread(pieces[0])
piece_height, piece_width, _ = piece_img.shape
img_height = piece_height * rows
img_width = piece_width * cols

# Making an empty canvas to put the new image on
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

# Putting all of the pieces together, math is kinda funky here
for i, piece_file in enumerate(pieces):
    piece = cv2.imread(piece_file)
    actual_height, actual_width, _ = piece.shape
    row = i // rows
    col = i % cols
    img[row*piece_height:row*piece_height+actual_height, col*piece_width:col*piece_width+actual_width] = piece

cv2.imwrite('pog.png', img)
