import audio_translate
import parse_by_kdxf
import parse_json
import lipRecognition
import os
import time


class AudioDialogueOutput(object):
    def __init__(self, input_file, output_file, appid, secret_key):
        self.input_file = input_file
        self.output_file = output_file
        self.appid = appid
        self.secret_key = secret_key

    def mkdir_output(self, output_dir):
        """
        判断是否需要创建新的文件夹
        :param output_dir:
        :return:
        """
        existence = os.path.exists(output_dir)
        if not existence:
            print('创建音频存放目录')
            os.makedirs(output_dir)  # 创建目录
            os.chdir(output_dir)  # 切换到创建的文件夹
            return True
        else:
            print('目录已存在,即将保存！')
            return False

    def aud_tr(self):
        """
        将视频中的音频输出，44kHZ,16bit,单声道
        :return:视频对应的音频
        """
        audio_translate.audio_translate(self.input_file, self.output_file)

    def kdxf(self):
        """
        将音频上传至科大讯飞进行语音识别
        :return:得到的识别结果保存为json格式数据。数据中包含语音识别结果，以及语音的开始、结束时间
        """
        #os.chdir(self.output_file + r'\audio\origin')
        filename = os.listdir(self.output_file + r'\audio\origin')  # 得到文件夹下的所有文件名称
        for fn in filename:
            api = parse_by_kdxf.RequestApi(appid=self.appid, secret_key=self.secret_key,
                                           upload_file_path=self.output_file + r'\audio\origin' + '\\'+fn,
                                           output_file=self.output_file + r'\dialogue\origin', filename=fn)
            api.all_api_request()

    def parse_js(self):
        """
        对时间戳进行解析，并对视频何音频进行切割
        :return: 切割后的音视频
        """
        #os.chdir(self.output_file + r'\dialogue\origin')
        # 重新存储的文件顺序可能被打乱，此时需要对文件进行查找
        filename_dialogue = os.listdir(self.output_file + r'\dialogue\origin')  # 得到文件夹下的所有文件名称
        filename_audio_origin = os.listdir(self.output_file + r'\audio\origin')
        filename_video_origin = os.listdir(self.input_file)
        fd = [''.join(i.split('.')[:-1]) for i in filename_dialogue]
        print(fd)
        fao = [''.join(i.split('.')[:-1]) for i in filename_audio_origin]
        print(fao)
        fvo = [''.join(i.split('.')[:-1]) for i in filename_video_origin]
        print(fvo)

        # 对文件夹中所有音视频进行切割
        for fn_d in fd:
            ao = self.output_file + r'\audio\origin\\' + filename_audio_origin[fao.index(fn_d)]
            print(ao)
            fn_path = self.output_file + r'\dialogue\origin\\' + fn_d
            vo = self.input_file + r'\\' + filename_video_origin[fvo.index(fn_d)]
            parse_json.par_js(fn_d, ao, vo, self.output_file,fn_path)


    def lip_video2frame(self):
        filename = os.listdir(self.output_file + r'\video')
        for fn in filename:
            lipRecognition.video2frame(self.output_file + r'\video\{}'.format(fn), self.output_file, ''.join(fn.split('.')[:-1]))  # 将视频转化成帧和大头照

    def lip_framecut(self):
        filename = os.listdir(self.output_file + r'\video')
        for fn in filename:
            lipRecognition.predict.predict(self.output_file + r'\video\{}'.format(fn), self.output_file, ''.join(fn.split('.')[:-1]))  # 将视频转化成帧和大头照

    def lip_coordinate(self):
        filename = os.listdir(self.output_file + r'\video')
        self.mkdir_output(self.output_file + r'\lip_coordinate')
        for fn in filename:
            lipRecognition.mouthdetect(self.output_file + r'\video\{}'.format(fn), self.output_file, ''.join(fn.split('.')[:-1]))  # 将视频转化成帧和大头照

    def run(self):
        # 在输出文件夹下面那创建唯一的文件夹
        self.output_file = self.output_file + r'\{}'.format(
            time.strftime("%Y-%m-%d-%A %H-%M-%S", time.localtime(time.time())))
        self.mkdir_output(self.output_file)
        self.aud_tr()  # 输出文件夹：audio
        self.kdxf()  # 输出文件夹：dialogue
        self.parse_js()  # 输出文件夹：video。可以用于下一步操作的文件这里面
        self.lip_video2frame()
        self.lip_framecut()
        self.lip_coordinate()


if __name__ == '__main__':
    data_process = AudioDialogueOutput(input_file=r'E:\lipsssssssss\13111',
                                       output_file=r'E:\lipsssssssss\output',
                                       appid="603c57fe", secret_key="46b84801453d1cbf51f0532288c929a1")
    data_process.run()
