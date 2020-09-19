"""
This file is for preprocessing of dataset.
Dataset: Mall and Subway entrance, exit dataset
Original dataset distribution link: https://drive.google.com/drive/folders/0B8GCEsD4YSIkajlTSTB2aGxYNGs
"""
import os
import cv2
import glob
pwd = os.getcwd()


def download_dataset():
    os.chdir(os.path.join(pwd, 'datasets'))
    os.system(
        'wget -O mall.tar https://cloud.amilab.dev/s/a7tpj6Pkr8tBbdg/download')
    os.makedirs('mall', exist_ok=True)
    print('Extracting archive file...')
    os.system('tar -xvf mall.tar -C mall')
    os.system('rm mall.tar')


def extract_video_frame():
    os.chdir(os.path.join(pwd, 'datasets', 'mall'))
    video_list = ['mall_1.AVI', 'mall_2.AVI', 'mall_3.AVI',
                  'subway_entrance_turnstiles.AVI', 'subway_exit_turnstiles.AVI']
    video_split_threshold = [
        [13741, 13866, 14010, 14083, 14275, 14382, 14490, 14807,14884, 15188, 15340, 15450, 15556, 15660, 15765, 15841, 15919, 16130, 16253, 16433],
        [1226, 6631, 8920, 9514, 9607, 9732, 9818, 9845, 10018, 10168, 10246, 10321, 10393, 10466, 10553, 10631, 10760],
        [2800, 3656, 5819, 6859, 6950, 7055, 7146, 7270, 7392, 7556, 7640, 7736, 7790, 7850, 7924, 8242, 8360, 8426, 8496, 12307, 13820],
        [5587 ,5950 ,7893 ,13848 ,13947 ,14761 ,14791 ,16689 ,16866 ,17300 ,17712 ,17947 ,20050 ,20050 ,23182 ,23240 ,23567 ,23810 ,24955 ,26124 ,13540 ,14419 ,14605 ,17160 ,19065 ,19343 ,23094 ,23519 ,23647 ,23857 ,25608],
        [8186 ,8296 ,8312 ,10095 ,10205 ,12037 ,12090 ,12112 ,12150],
    ]

    for video_path in video_list:
        os.makedirs(os.path.splitext(video_path)[0] + '_train', exist_ok=True)
        os.makedirs(os.path.splitext(video_path)[0] + '_test', exist_ok=True)
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
    # extract_video_frame()
    # save_gt_to_img()
