import subprocess
import shutil
import os
from img_resize import img_resize
from culc_feachers import features_culk
import cv2
import datetime
from insert_dist_coeff import change_camera_params_in_json

file = open("result/time_res.txt", "w")

step = 1
rk = 4.0
#steps = [1, 2, 3, 5]
#r_koefs = [1, 1.5, 2.0, 4.0]
r_koefs = [4.0]
steps = [5]
for step in steps:
    for rk in r_koefs:
        I_PATH = "./raw_images"
        img_name = "IMG_{0}.jpg".format(1568)
        i_file = os.path.join(I_PATH, img_name)
        img = cv2.imread(i_file, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
        width = int(img.shape[1] / rk)
        height = int(img.shape[0] / rk)
        num = 183 / step
        step_name = "Count of images: {0} Width: {1} Height: {2}\n".format(num, width, height)
        file.write(step_name)

        o_path = './dest'
        shutil.rmtree(o_path)
        if not os.path.exists(o_path):
            os.makedirs(o_path)
        cmdline = []
        cmdline.append("python")
        cmdline.append("MvgMvs_Pipeline.py")
        cmdline.append("images")
        cmdline.append("dest")
        cmdline.append("-f")
        cmdline.append("0")
        cmdline.append("-l")
        cmdline.append("4")

        img_resize(step, rk)
        cmdline[5] = "0"
        cmdline[7] = "0"
        pStep = subprocess.Popen(cmdline)
        pStep.wait()
        change_camera_params_in_json("/home/titan/openmvs/openMVS_sample/dest/matches/sfm_data.json",
                                     "/home/titan/openmvs/openMVS_sample/dest/matches/sfm_data.json",
                                     key="ARKIT")
        start_time = datetime.datetime.now().time()
        cmdline[5] = "1"
        cmdline[7] = "1"
        pStep = subprocess.Popen(cmdline)
        pStep.wait()
        end_time = datetime.datetime.now().time()
        min = end_time.minute - start_time.minute
        sec = end_time.second - start_time.second
        d_time = min * 60 + sec
        com_f = "Compute features: {0} seconds\n".format(d_time)
        file.write(com_f)
        start_time = datetime.datetime.now().time()
        cmdline[5] = "2"
        cmdline[7] = "2"
        pStep = subprocess.Popen(cmdline)
        pStep.wait()
        end_time = datetime.datetime.now().time()
        min = end_time.minute - start_time.minute
        sec = end_time.second - start_time.second
        d_time = min * 60 + sec
        com_f = "Compute matches: {0} seconds\n".format(d_time)
        file.write(com_f)
        cmdline[5] = "3"
        cmdline[7] = "4"
        pStep = subprocess.Popen(cmdline)
        pStep.wait()


        res_path = "./result"
        if not os.path.exists(res_path):
            os.makedirs(res_path)
        features_culk(step, rk, res_path)
        raw_cloud = "cloud_and_poses.ply"
        raw_color = "colorized.ply"
        num = 183 / step
        res_name =  "{0}_{1}x{2}_".format(num, width, height)
        res_cloud = res_name + raw_cloud
        res_color = res_name + raw_color
        recons_path = "./dest/reconstruction_sequential"
        cloud_path = os.path.join(recons_path, raw_cloud)
        res_cloud_path = os.path.join(res_path, res_cloud)
        color_path = os.path.join(recons_path, raw_color)
        res_color_path = os.path.join(res_path, res_color)
        os.rename(cloud_path, res_cloud_path)
        os.rename(color_path, res_color_path)

file.close()