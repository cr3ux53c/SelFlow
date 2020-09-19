"""
This file is for preprocessing of dataset.
Dataset: Avenue
Original dataset distribution link: http://www.cse.cuhk.edu.hk/leojia/projects/detectabnormal/dataset.html
"""
import os
import cv2
import glob
pwd = os.getcwd()


def download_dataset():
    os.chdir(os.path.join(pwd, 'datasets'))
    os.system(
        'wget -O avenue.tar https://cloud.amilab.dev/s/tYgdTtQNjPP8irn/download')
    os.makedirs('avenue', exist_ok=True)
    print('Extracting archive file...')
    os.system('tar -xvf avenue.tar -C avenue')


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


if __name__ == "__main__":
    download_dataset()
    extract_video_frame()
    save_gt_to_img()
