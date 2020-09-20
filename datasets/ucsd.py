"""
This file is for preprocessing of dataset.
Dataset: UCSD Anomaly Detection Dataset
Original dataset distribution link: http://www.svcl.ucsd.edu/projects/anomaly/dataset.html
"""
import re
import os
import cv2
import glob
pwd = os.getcwd()


def download_dataset(delete_archive=False):
    os.chdir(os.path.join(pwd, 'datasets'))
    if not os.path.isfile('ucsd.tar'):
        os.system(
            'wget -O ucsd.tar https://cloud.amilab.dev/s/BxfcCnCgEyiZaC4/download')
    os.makedirs('ucsd', exist_ok=True)
    print('Extracting archive file...')
    os.system('tar -xvf ucsd.tar -C ucsd')
    if delete_archive:
        os.system('rm ucsd.tar')


def convert_tif_to_png():
    os.chdir(os.path.join(pwd, 'datasets', 'ucsd'))

    for root_dir in ['UCSDped1', 'UCSDped2']:
        for sub_dir in ['Test', 'Train']:
            for index in range(1, 37):
                frame_list = glob.glob(os.path.join(
                    root_dir, sub_dir, sub_dir + '{:03d}'.format(index), '*.tif'))
                for frame_path in frame_list:
                    print(
                        'Save tif to png file of video sequence #{:04d}...'.format(index))
                    img = cv2.imread(frame_path)
                    cv2.imwrite(os.path.splitext(frame_path)[0] + '.png', img)


def copy_all_seqeunce_to_one_folder():
    from shutil import copyfile

    os.chdir(os.path.join(pwd, 'datasets', 'ucsd'))

    for root_dir in ['UCSDped1', 'UCSDped2']:
        for sub_dir in ['Test', 'Train']:
            os.makedirs(os.path.join(root_dir, sub_dir + 'All'), exist_ok=True)
            for index in range(1, 37):
                if sub_dir == 'Test':
                    if os.path.isdir(os.path.join(root_dir, sub_dir, sub_dir + '{:03d}_gt'.format(index))) == False:
                        continue

                frame_list = glob.glob(os.path.join(
                    root_dir, sub_dir, sub_dir + '{:03d}'.format(index), '*.png'))
                for frame_path in frame_list:
                    print(
                        'Save copies of video frames #{:04d}...'.format(index))
                    copyfile(frame_path, os.path.join(root_dir, sub_dir + 'All',
                                                      sub_dir + str(index) + '_' + os.path.basename(frame_path)))


def create_imgfile_list():
    os.chdir(os.path.join(pwd, 'datasets', 'ucsd'))
    result_dir = '../../img_list'

    for sub_dir in ['UCSDped1', 'UCSDped2']:
        for sub_sub_dir in ['TestAll', 'TrainAll']:
            list_file = open(os.path.join(
                result_dir, sub_dir + '_' + sub_sub_dir + '.txt'), 'w')

            preprevious_img = None
            previous_img = None
            count = 0
            count += 1  # forward_of => 002.png with 003.png
            for img in sorted(sorted(glob.glob(os.path.join(sub_dir, sub_sub_dir, '*.png')),
                                     key=lambda x: (int(x.partition('/')[2].partition('/')[2][sub_sub_dir.partition('A')[0].__len__():].partition('_')[0]))),
                              key=lambda x: (int(x.partition('/')[2].partition('/')[2][sub_sub_dir.partition('A')[0].__len__():].partition('_')[0])) * 10000 + int(str(x.partition('_')[2].partition('.')[0]))):
                print('Listing {}...'.format(img))
                if preprevious_img is None:
                    preprevious_img = os.path.basename(img)
                    continue

                if previous_img is None:
                    previous_img = os.path.basename(img)
                    continue

                count += 1

                list_file.write(preprevious_img + ' ' + previous_img +
                                ' ' + os.path.basename(img) + ' {:04d}\n'.format(count))
                preprevious_img = previous_img
                previous_img = os.path.basename(img)


if __name__ == "__main__":
    # download_dataset()
    # convert_tif_to_png()
    # copy_all_seqeunce_to_one_folder()
    create_imgfile_list()
