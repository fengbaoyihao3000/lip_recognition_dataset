import os
from ffmpy3 import FFmpeg


def mkdir_output(output_dir):
    existence = os.path.exists(output_dir)
    if not existence:
        #print('创建存放目录')
        os.makedirs(output_dir)  # 创建目录
        os.chdir(output_dir)  # 切换到创建的文件夹
        return True
    else:
        #print('目录已存在,即将保存！')
        return False


def audio_translate(filepath, output_dir):
    os.chdir(filepath)  # 切换到改路径下
    filename = os.listdir(filepath)  # 得到文件夹下的所有文件名称
    output_dir = output_dir + r'\audio\origin'  # 转换后音频文件存放的路径
    mkdir_output(output_dir)
    for i in range(len(filename)):
        # 当输出文件名存在时可能会报错，此时需要进行覆盖
        try:
            changefile = filepath + "\\" + filename[i]
            outputfile = output_dir + "\\" + filename[i].replace('mp4', 'wav').replace('mkv', 'wav') \
                .replace('rmvb', 'wav').replace('3gp', 'wav').replace('avi', 'wav') \
                .replace('mpeg', 'wav').replace('mpg', 'wav').replace('dat', 'asf') \
                .replace('wmv', 'wav').replace('flv', 'wav').replace('mov', 'wav') \
                .replace('mp4', 'wav').replace('ogg', 'wav').replace('ogm', 'wav') \
                .replace('rm', 'wav')
            ff = FFmpeg(
                inputs={changefile: None},
                outputs={outputfile: '-vn -ar 44100 -ac 2 -ab 192 -f wav'}
            )
            #print(ff.cmd)
            ff.run()
        except Exception:
            continue
