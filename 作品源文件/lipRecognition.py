import cv2
import shutil
import os
import colorsys
import copy
import math
import time
import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
from PIL import Image, ImageDraw, ImageFont
from torch.nn import functional as F
from nets.frcnn import FasterRCNN
from nets.frcnn_training import get_new_img_size
from utils.utils import DecodeBox, loc2bbox, nms
from PIL import ImageFile
import predict
import sys
'''原视频放在source_video_path下，分割后的帧放在frames文件夹下，合并后的视频放在video文件夹下'''


def mkdir_output(output_dir):
    """
    判断是否需要创建新的文件夹
    :param output_dir:
    :return:
    """
    existence = os.path.exists(output_dir)
    if not existence:
        #print('创建存放目录')
        os.makedirs(output_dir)  # 创建目录
        os.chdir(output_dir)  # 切换到创建的文件夹
        return True
    else:
        #print('目录已存在,即将保存！')
        return False


# 把视频分为帧
def video2frame(input_file, output_file, fn):
    cap = cv2.VideoCapture(input_file)  # 读取原视频
    # print(input_file)
    mkdir_output(output_file + r'\frame\{}'.format(fn))
    c = 1  # 文件名从1开始
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 原视频总帧数
    # print("frame_count={}".format(frame_count))
    numFrame = 0
    while c <= frame_count:
        if cap.grab():
            flag, frame = cap.retrieve()
            if not flag:
                continue
            else:
                # cv2.imshow('video', frame)
                numFrame += 1
                path = output_file + r'\frame\{}'.format(fn) + r'\\' + str(numFrame) + '.jpg'
                cv2.imencode('.jpg', frame)[1].tofile(path)
        c += 1
    cap.release()
    cv2.destroyAllWindows()


# 识别嘴唇并输出嘴唇坐标
def mouthdetect(input_file, output_file, fn):
    #pic_path = output_file + r'\face_frames\{}\\'.format(fn)+'/face_frames/'+str(fn)
    pic_path = output_file + '/face_frames/' + str(fn) + '/'
    # 加载haar级联分类器
    mouth_cascade = cv2.CascadeClassifier(sys.path[0]+'/model/haarcascade_mcs_lip.xml')
    #print(sys.path[0])
    frame = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_COUNT))
    f = open(output_file + r'\lip_coordinate\{}_coordinate.txt'.format(fn), "w")  # 创建并打开lip_position.txt
    for i in range(1, frame):
        picname = pic_path + str(i) + '.jpg'
        if(os.path.exists(picname)):
            # 读取进行检测的图像
            img = cv2.imread(picname)
            # img = np.astype('uint8')
            # 将原图像转为灰度图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 使用级联分类器进行嘴唇检测 返回值为 嘴唇的bounding box参数（左上角坐标（x,y），矩形框长和宽）
            try:
                mouths = mouth_cascade.detectMultiScale(gray, scaleFactor=1.3,
                                                        minNeighbors=40)  # 第三个参数为minNeighbors，数值越大越准确，但是可能识别不出
                # 绘制矩形框
                for (x, y, w, h) in mouths:
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    #print(str(i) + '.jpg', end=" ")
                    #print(x, y, x + w, y + h)
                    f.write(str(i) + '.jpg' + ' ')
                    f.write(str(x) + ' ' + str(y) + ' ' + str(x + w) + ' ' + str(y + h) + '\n')
            except Exception:
                pass
        else:
            continue


        # # 显示检测结果
        # cv2.namedWindow('mouthDetection')
        # cv2.imshow('mouthDetection', img)
        # time.sleep(5)
        # cv2.destroyAllWindows()

# 把帧合成视频
# def frame2video():
#     image = cv2.imread('./frames/1.jpg')  # 获取一张图片的宽高作为视频的宽高
#     source_video = cv2.VideoCapture('./source_video_path/1.mp4')  # 读取原视频
#     fps = source_video.get(cv2.CAP_PROP_FPS)  # 获得视频的帧率
#     frames = int(source_video.get((cv2.CAP_PROP_FRAME_COUNT)))  # 获得视频总帧数
#
#     # 获取视频的尺寸
#     image_info = image.shape
#     height = image_info[0]
#     width = image_info[1]
#     size = (height, width)
#
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 视频输出的格式
#     video = cv2.VideoWriter('./videos/1.mp4', fourcc, fps, (width, height))
#     for i in range(1, frames):
#         file_name = './frames/' + str(i) + '.jpg'
#         image = cv2.imread(file_name)
#         video.write(image)  # 向视频文件写入一帧--只有图像,没有声音
#     cv2.waitKey()


# video2frame()
# predict.predict()
# mouthdetect()
