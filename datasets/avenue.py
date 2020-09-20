"""
This file is for preprocessing of dataset.
Dataset: Avenue
Original dataset distribution link: http://www.cse.cuhk.edu.hk/leojia/projects/detectabnormal/dataset.html
"""
import os
import cv2
import glob
pwd = os.getcwd()
DATASET_NAME = 'avenue'


def download_dataset(delete_archive=False):
    os.chdir(os.path.join(pwd, 'datasets'))
    if not os.path.isfile('avenue.tar'):
        os.system(
            'wget -O avenue.tar https://cloud.amilab.dev/s/tYgdTtQNjPP8irn/download')
    os.makedirs('avenue', exist_ok=True)
    print('Extracting archive file...')
    os.system('tar -xvf avenue.tar -C avenue')
    if delete_archive:
        os.system('rm avenue.tar')


def extract_video_frame():
    os.chdir(os.path.join(pwd, 'datasets', 'avenue'))
    for video_dir in ['testing_videos', 'training_videos']:
        video_dir = os.path.join(os.getcwd(), video_dir)
        video_list = sorted(glob.glob(os.path.join(video_dir, '*.avi')))

        for video_path in video_list:
            os.makedirs(os.path.splitext(video_path)[0], exist_ok=True)
            vidcap = cv2.VideoCapture(video_path)
            readable, frame = vidcap.read()
            count = 0
            while readable:
                print('Extracting frame {:04d}'.format(count))
                cv2.imwrite(os.path.join(os.path.splitext(video_path)[
                            0], '{:04d}.png'.format(count)), frame)
                readable, frame = vidcap.read()
                count += 1


def save_gt_to_img():
    import scipy.io
    import numpy as np

    os.chdir(os.path.join(pwd, 'datasets', 'avenue',
                          'ground_truth_demo', 'testing_label_mask'))
    mat_list = sorted(glob.glob('*.mat'))

    for mat_path in mat_list:
        mat = scipy.io.loadmat(mat_path)
        # np.save(os.path.splitext(os.path.basename(mat_path))[0] + '.npy', mat['volLabel'])
        os.makedirs(os.path.splitext(
            os.path.basename(mat_path))[0], exist_ok=True)

        for i in range(mat['volLabel'][0].size):
            print('Saving thresholded image #{:04d}...'.format(i))
            ret, res = cv2.threshold(
                mat['volLabel'][0][i], 0, 255, cv2.THRESH_BINARY)
            cv2.imwrite(os.path.join(os.path.splitext(
                os.path.basename(mat_path))[0], '{:04d}.png'.format(i)), res)


def create_imgfile_list():
    os.chdir(os.path.join(pwd, 'datasets', 'avenue'))
    result_dir = '../../img_list'

    for sub_dir in ['testing_videos', 'training_videos']:
        list_file = open(os.path.join(result_dir, 'avenue_' + sub_dir + '.txt'), 'w')

        preprevious_img = None
        previous_img = None
        count = 0
        count += 1  # forward_of => 002.png with 003.png
        for img in sorted(sorted(glob.glob(os.path.join(sub_dir + '_All', '*.png')))):
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


def copy_all_seqeunce_to_one_folder():
    from shutil import copyfile

    os.chdir(os.path.join(pwd, 'datasets', DATASET_NAME))

    for root_dir in ['testing_videos', 'training_videos']:
        for index in range(1, 22):
            index = str(index).zfill(2)
            os.makedirs(os.path.join(root_dir + '_All'), exist_ok=True)

            frame_list = sorted(glob.glob(os.path.join(root_dir, index, '*.png')))
            for frame_path in frame_list:
                print(
                    'Save copies of video frames #{}...'.format(index))
                copyfile(frame_path, os.path.join(root_dir + '_All', index + '_' + os.path.basename(frame_path)))



if __name__ == "__main__":
    # download_dataset()
    # extract_video_frame()
    # copy_all_seqeunce_to_one_folder()
    # save_gt_to_img()
    create_imgfile_list()
