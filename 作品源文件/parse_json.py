import json, jsonpath, os, shutil
from pydub import AudioSegment
from moviepy.editor import *
from moviepy.editor import VideoFileClip


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


def video_cut(original_file, new_file, start_time, end_time):
    """
    对视频进行切割并输出
    :param original_file: 原始视频路径
    :param new_file: 输出视频路径
    :param start_time: 视频开始剪辑时间
    :param end_time: 视频结束剪辑时间
    :return: 剪切后的视频
    """
    video = VideoFileClip(original_file).subclip(start_time, end_time)
    result = video.write_videofile(new_file)
    return result


def par_js(fn_d, fn_ao, fn_vo, output_file,fn_path):
    """
    解析json文件中的起始、结束时间，对音视频进行分割
    :param fn_d: json文件名
    :param fn_ao: 原始音频文件路径
    :param fn_vo: 原始视频文件路径
    :param output_file: 输出文件夹路径
    :return:
    """
    fn_dname = fn_d
    fn_d = fn_path + '.json'

    # 读取json数据
    with open(fn_d, 'r', encoding='UTF-8') as f:
        fn_d = json.loads(f.read())
        fn_d['data'] = eval(fn_d['data'])
    audio_file = fn_ao
    video_file = fn_vo
    # 读取音频数据
    audio = AudioSegment.from_wav(audio_file)
    # 读取起始、结束时间戳
    list_of_timestamp_start = list(map(int, jsonpath.jsonpath(fn_d, '$..bg')))  # and so on in *seconds*
    list_of_timestamp_end = list(map(int, jsonpath.jsonpath(fn_d, '$..ed')))
    dialogue_list = jsonpath.jsonpath(fn_d, '$..onebest')

    # 创建文件夹
    output_video = output_file + r'\video'
    output_audio_split = output_file + r'\audio\split'
    output_dialogue_split = output_file + r'\dialogue\split'
    mkdir_output(output_video)
    mkdir_output(output_audio_split)
    mkdir_output(output_dialogue_split)

    # 对音视频进行剪切
    for start, end, dialogue in zip(list_of_timestamp_start, list_of_timestamp_end, dialogue_list):
        #print("split at [ {}:{}] ms".format(start, end))
        video_cut(video_file, output_video + r"\{}_chunk_{}.mp4".format(fn_dname, end), start / 1000, end / 1000)
        audio_chunk = audio[start:end]
        audio_chunk.export(output_audio_split + r"\{}_chunk_{}.wav".format(fn_dname, end), format="wav")
        with open(output_dialogue_split + r"\{}_chunk_{}.txt".format(fn_dname, end), 'w') as f:
            f.write(dialogue)
    #print('over')


if __name__ == "__main__":
    par_js()
