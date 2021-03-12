#-------------------------------------#
#           对图片进行预测
#-------------------------------------#
from PIL import Image
import colorsys
import copy
import math
import os
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
import shutil
import sys
def mkdir_output(output_dir):
    """
    判断是否需要创建新的文件夹
    :param output_dir:
    :return:
    """
    existence = os.path.exists(output_dir)
    if not existence:
        print('创建存放目录')
        os.makedirs(output_dir)  # 创建目录
        os.chdir(output_dir)  # 切换到创建的文件夹
        return True
    else:
        print('目录已存在,即将保存！')
        return False

def predict(input_file,output_file,fn):
    class FRCNN(object):
        _defaults = {
            "model_path": 'model/Epoch30-Total_Loss0.8104-Val_Loss0.7883.pth',  # 模型的位置
            "classes_path": 'model_data/voc_classes.txt',  # 分类的标签
            "confidence": 0.6,
            "iou": 0.01,
            "backbone": "resnet50",
            "cuda": True,
        }

        @classmethod
        def get_defaults(cls, n):
            if n in cls._defaults:
                return cls._defaults[n]
            else:
                return "Unrecognized attribute name '" + n + "'"

        # ---------------------------------------------------#
        #   初始化faster RCNN
        # ---------------------------------------------------#
        def __init__(self, **kwargs):
            self.__dict__.update(self._defaults)
            self.class_names = self._get_class()
            self.generate()
            self.mean = torch.Tensor([0, 0, 0, 0]).repeat(self.num_classes + 1)[None]
            self.std = torch.Tensor([0.1, 0.1, 0.2, 0.2]).repeat(self.num_classes + 1)[None]
            if self.cuda:
                self.mean = self.mean.cuda()
                self.std = self.std.cuda()

        # ---------------------------------------------------#
        #   获得所有的分类
        # ---------------------------------------------------#
        def _get_class(self):
            #classes_path =os.path.expanduser(self.classes_path)
            #classes_path = os.getcwd() + r'\\' + os.path.expanduser(self.classes_path)
            classes_path = sys.path[0] + '/' + os.path.expanduser(self.classes_path)
            with open(classes_path) as f:
                class_names = f.readlines()
            class_names = [c.strip() for c in class_names]
            return class_names

        # ---------------------------------------------------#
        #   获得所有的分类
        # ---------------------------------------------------#
        def generate(self):
            # 计算总的种类
            self.num_classes = len(self.class_names)

            # 载入模型，如果原来的模型里已经包括了模型结构则直接载入。
            self.model = FasterRCNN(self.num_classes, "predict", backbone=self.backbone)
            print('Loading weights into state dict...')
            device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            state_dict = torch.load(sys.path[0]+'/'+self.model_path, map_location=device)
            self.model.load_state_dict(state_dict)

            self.model = self.model.eval()

            if self.cuda:
                os.environ["CUDA_VISIBLE_DEVICES"] = '0'
                self.model = nn.DataParallel(self.model)
                self.model = self.model.cuda()

            print('{} model, anchors, and classes loaded.'.format(self.model_path))

            # 画框设置不同的颜色
            hsv_tuples = [(x / len(self.class_names), 1., 1.)
                          for x in range(len(self.class_names))]
            self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
            self.colors = list(
                map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                    self.colors))

        # ---------------------------------------------------#
        #   检测图片
        # ---------------------------------------------------#
        def detect_image(self, image):
            #global left,top,right,bottom
            with torch.no_grad():
                start_time = time.time()
                image_shape = np.array(np.shape(image)[0:2])
                old_width = image_shape[1]
                old_height = image_shape[0]
                old_image = copy.deepcopy(image)
                width, height = get_new_img_size(old_width, old_height)

                image = image.resize([width, height], Image.BICUBIC)
                photo = np.array(image, dtype=np.float32) / 255
                photo = np.transpose(photo, (2, 0, 1))

                images = []
                images.append(photo)
                images = np.asarray(images)
                images = torch.from_numpy(images)
                if self.cuda:
                    images = images.cuda()

                roi_cls_locs, roi_scores, rois, roi_indices = self.model(images)
                decodebox = DecodeBox(self.std, self.mean, self.num_classes)
                outputs = decodebox.forward(roi_cls_locs, roi_scores, rois, height=height, width=width,
                                            nms_iou=self.iou,
                                            score_thresh=self.confidence)
                if len(outputs) == 0:
                    return old_image
                bbox = outputs[:, :4]
                conf = outputs[:, 4]
                label = outputs[:, 5]

                bbox[:, 0::2] = (bbox[:, 0::2]) / width * old_width
                bbox[:, 1::2] = (bbox[:, 1::2]) / height * old_height
                bbox = np.array(bbox, np.int32)

            image = old_image
            thickness = (np.shape(old_image)[0] + np.shape(old_image)[1]) // old_width * 2
            font = ImageFont.truetype(font='model_data/simhei.ttf',
                                      size=np.floor(3e-2 * np.shape(image)[1] + 0.5).astype('int32'))

            for i, c in enumerate(label):
                predicted_class = self.class_names[int(c)]
                score = conf[i]

                left, top, right, bottom = bbox[i]
                top = top - 5
                left = left - 5
                bottom = bottom + 5
                right = right + 5

                top = max(0, np.floor(top + 0.5).astype('int32'))
                left = max(0, np.floor(left + 0.5).astype('int32'))
                bottom = min(np.shape(image)[0], np.floor(bottom + 0.5).astype('int32'))
                right = min(np.shape(image)[1], np.floor(right + 0.5).astype('int32'))


            return image,left,top,right,bottom

    frcnn = FRCNN()

    source_video = cv2.VideoCapture(input_file)  # 读取原视频
    frames = int(source_video.get(cv2.CAP_PROP_FRAME_COUNT))  # 获得原视频总帧数
    i = 1
    mkdir_output(output_file + r'\face_frames\{}'.format(fn))
    for i in range(1, frames):
        img = output_file + r'\frame\{}\\'.format(fn) + str(i) + '.jpg'
        image = Image.open(img)
        image = image.convert("RGB")
        try:
            r_image,left,top,right,bottom = frcnn.detect_image(image)
            #print(i, left, top, right, bottom)
            r_image = r_image.crop((0.9 * left, 0.9 * top, right, 1.1 * bottom))
            # r_image.show()
            r_image.save(output_file + r'\face_frames\{}\\'.format(fn) + str(i) + '.jpg')  #
        except Exception:
            continue




