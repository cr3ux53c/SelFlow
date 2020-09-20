"""
This file is for preprocessing of dataset.
Dataset: UMN Dataset
Original dataset distribution link: https://www.crcv.ucf.edu/projects/Abnormal_Crowd/
"""
import re
import os
import cv2
import glob
pwd = os.getcwd()
DATASET_NAME = 'umn'


def download_dataset(delete_archive=False):
    os.chdir(os.path.join(pwd, 'datasets'))
    if not os.path.isfile(DATASET_NAME + '.tar'):
        os.system(
            'wget -O ' + DATASET_NAME + '.tar https://cloud.amilab.dev/s/AdMzpiYHtSBng2e/download')
    os.makedirs(DATASET_NAME, exist_ok=True)
    print('Extracting archive file...')
    os.system('tar -xvf ' + DATASET_NAME + '.tar -C ' + DATASET_NAME)
    if delete_archive:
        os.system('rm ' + DATASET_NAME + '.tar')


def extract_video_frame():
    os.chdir(os.path.join(pwd, 'datasets', DATASET_NAME))
    video_list = sorted(glob.glob(os.path.join('*.avi')))

    for video_path in video_list:
        os.makedirs(os.path.splitext(video_path)[0], exist_ok=True)
        vidcap = cv2.VideoCapture(video_path)
        readable, frame = vidcap.read()
        count = 0
        while readable:
            print('Extracting frame {:04d}'.format(count))
            cv2.imwrite(os.path.join(os.path.splitext(video_path)
                                     [0], '{:04d}.png'.format(count)), frame)
            readable, frame = vidcap.read()
            count += 1


def create_imgfile_list():
    os.chdir(os.path.join(pwd, 'datasets', DATASET_NAME))
    result_dir = '../../img_list'


    for chapter in [1, 2, 3, 4]:
        for split in ['Test', 'Train']:
            list_file = open(os.path.join(result_dir, 'Crowd_Activity_Chapter' + str(chapter) + '_' + split + '.txt'), 'w')

            preprevious_img = None
            previous_img = None
            count = 0
            count += 1  # forward_of => 002.png with 003.png
            for img in sorted(glob.glob(os.path.join('Crowd_Activity_Chapter' + str(chapter) + '_' + split, '*.png'))):
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
    # extract_video_frame()
    create_imgfile_list()
