import cv2
import os
import piexif
import shutil

def img_resize(step, rk):
    I_PATH = "./raw_images"
    O_PATH = "./images"

    shutil.rmtree(O_PATH)
    if not os.path.exists(O_PATH):
        os.makedirs(O_PATH)

    for num in range(1568, 1751, step):
        img_name = "IMG_{0}.jpg".format(num)
        i_file = os.path.join(I_PATH, img_name)
        o_file = os.path.join(O_PATH, img_name)
        img = cv2.imread(i_file, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)

        width = int(img.shape[1] / rk)
        height = int(img.shape[0] / rk)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(o_file, resized)
        piexif.transplant(i_file, o_file)
        print img_name