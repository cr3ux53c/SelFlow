import sys, os, glob

list_filename = 'stairs.txt'
dataset_dir = 'stairs/testAll'

f = open(os.path.join('img_list', list_filename), mode='wt')

dataset_list = sorted(glob.glob(os.path.join('datasets', dataset_dir, '*.jpg')))
prev_prev_imgfile = ''
prev_imgfile = ''
for idx, img_file in enumerate(dataset_list):
    if prev_imgfile == '':
        prev_imgfile = os.path.basename(img_file)
        continue
    if prev_prev_imgfile == '':
        prev_prev_imgfile = prev_imgfile
        prev_imgfile = os.path.basename(img_file)
        continue
    
    f.write('{} {} {} {:04d}\n'.format(prev_prev_imgfile, prev_imgfile, os.path.basename(img_file), idx))
    prev_prev_imgfile = prev_imgfile
    prev_imgfile = os.path.basename(img_file)

f.close()