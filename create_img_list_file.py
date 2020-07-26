import os
from os.path import join
import glob


data_dir = 'images/ucsdped1_test'

f = open('img_list/ucsdped1_test.txt', 'w')

preprevious_img = None
previous_img = None
count = 0
count += 1  # forward_of => 002.png with 003.png
for img in sorted(glob.glob(join(data_dir, '*.png'))):
    
    if preprevious_img is None:
        preprevious_img = os.path.basename(img)
        continue
    
    if previous_img is None:
        previous_img = os.path.basename(img)
        continue
    
    count += 1

    f.write(preprevious_img + ' ' + previous_img + ' ' + os.path.basename(img) + ' {:04d}\n'.format(count))
    preprevious_img = previous_img
    previous_img = os.path.basename(img)