# 因为bilibili限制上传文件最大为16G
# 检测指定目录下的视频文件, 如果大小大于16G, 则不停的进行二分分割

import os
from moviepy.editor import VideoFileClip

root_dir = '/media/zx/新加卷/Video'
max_size = 16
continue_flag = False


def get_video_size(path):
    # G
    return os.path.getsize(path) / 1024 / 1024 / 1024


def get_video_length(path):
    # s
    return int(VideoFileClip(path).duration) + 1


def convert_time(time):
    # example
    # 3662 -> 01:01:02
    #  int ->   str
    h = str(time // 3600)
    s = str(time % 60)
    m = str((time - int(h) * 3600) // 60)

    if len(h) < 2:
        h = '0' + h
    if len(m) < 2:
        m = '0' + m
    if len(s) < 2:
        s = '0' + s

    return h + ':' + m + ':' + s


def ffmpeg_split(path, start, during, new_path):
    command = 'ffmpeg -ss ' + convert_time(start) + ' -t ' + convert_time(
        during) + ' -i ' + '"' + path + '"' + ' -vcodec copy -acodec copy ' + '"' + new_path + '"'
    os.system(command)


def split(path):
    stack = [path]
    while stack:
        now_file_path = stack.pop()
        if get_video_size(now_file_path) > max_size:
            video_length = get_video_length(now_file_path)
            during = video_length // 2
            new1 = now_file_path[:-4] + '_1' + now_file_path[-4:]
            new2 = now_file_path[:-4] + '_2' + now_file_path[-4:]
            ffmpeg_split(now_file_path, 0, during, new1)
            ffmpeg_split(now_file_path, during, during + 1, new2)
            stack.append(new1)
            stack.append(new2)
        else:
            continue


list_dir = os.listdir(path=root_dir)

for i in list_dir:
    f_path = root_dir + '/' + i
    if os.path.isfile(f_path) and get_video_size(f_path) > max_size:

        if not continue_flag:
            print(f_path, get_video_size(f_path))
            ans = input('continue(y/n)\n')
            if ans == 'y':
                pass
            else:
                break

        split(f_path)
