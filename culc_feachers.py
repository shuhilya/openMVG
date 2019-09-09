import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import cv2



def features_culk(step, rk, res_path):
    count = 0
    FEAT_PATH = "./dest/matches"
    feat_list = []
    for num in range(1568, 1751, step):
        file_name = "IMG_{0}.feat".format(num)
        file_path = os.path.join(FEAT_PATH, file_name)
        num_lines = sum(1 for line in open(file_path))
        feat_list.append(num_lines)
        count += 1

    I_PATH = "./raw_images"
    img_name = "IMG_{0}.jpg".format(num)
    i_file = os.path.join(I_PATH, img_name)
    img = cv2.imread(i_file, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    width = int(img.shape[1] / rk)
    height = int(img.shape[0] / rk)


    sns.set(color_codes=True)
    fig = plt.figure()
    sns.distplot(feat_list, kde=False)
    plt.xlabel("Feature's count")
    plt.ylabel("Count")
    hist_title = "Size: {0}x{1} images: {2}".format(width, height, count)
    plt.title(hist_title)
    #plt.show()
    hist_name = "Size: {0}x{1} images: {2}".format(width, height, count)
    hist_name = os.path.join(res_path, hist_name)
    fig.savefig(hist_name)
