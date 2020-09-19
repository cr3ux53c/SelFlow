"""
This file is for preprocessing of dataset.
Dataset: UCSD Anomaly Detection Dataset
Original dataset distribution link: http://www.svcl.ucsd.edu/projects/anomaly/dataset.html
"""
import os
import cv2
import glob
pwd = os.getcwd()


def download_dataset():
    os.chdir(os.path.join(pwd, 'datasets'))
    os.system(
        'wget -O ucsd.tar https://cloud.amilab.dev/s/BxfcCnCgEyiZaC4/download')
    os.makedirs('ucsd', exist_ok=True)
    print('Extracting archive file...')
    os.system('tar -xvf ucsd.tar -C ucsd')
    os.system('rm ucsd.tar')


def convert_tif_to_png():
    os.chdir(os.path.join(pwd, 'datasets', 'ucsd'))

    for root_dir in ['UCSDped1', 'UCSDped2']:
        for sub_dir in ['Test', 'Train']:
            for index in range(1, 37):
                frame_list = glob.glob(os.path.join(
                    root_dir, sub_dir, sub_dir + '{:03d}'.format(index), '*.tif'))
                for frame_path in frame_list:
                    print('Save tif to png file of video sequence #{:04d}...'.format(index))
                    img = cv2.imread(frame_path)
                    cv2.imwrite(os.path.splitext(frame_path)[0] + '.png', img)


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
    convert_tif_to_png()
    # save_gt_to_img()
