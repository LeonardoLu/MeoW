import os
import re
import time

import functools
import json

from imghdr import what

from PIL import Image as image

def spilt_tex(tex_file, group, name, save_path):
    if what(tex_file) == "png":
        img = image.open(tex_file)
    else:
        return group

    os.makedirs(f"{save_path}/out/{name}", exist_ok=True)
    for var in group.keys():
        try:
            xy = group[var]['xy']
            size = group[var]['size']

            if group[var]['rotate']:
                rect = (xy[0], xy[1], size[1] + xy[0], size[0] + xy[1])
            else:
                rect = (xy[0], xy[1], size[0] + xy[0], size[1] + xy[1])

            val = img.crop(rect)
            if group[var]['rotate']:
                val = val.rotate(-90, expand=True)

            group[var]['pic'] = val
            var = var.replace("/", "-")
            path = f"{save_path}/out/{name}/{var}.png"
            val.save(path)
        except Exception as info:
            print(info)
            raise

    return group


def pos_spilt(file: str):
    info_pattern = re.compile(r'(.+)\n'
                              r'\s{2}rotate:\s(false|true)\n'
                              r'\s{2}xy:\s(\d+),\s(\d+)\n'
                              r'\s{2}size:\s(\d+),\s(\d+)\n'
                              r'\s{2}orig:\s\d+,\s\d+\n'
                              r'\s{2}offset:\s0,\s0\n'
                              r'\s{2}index:\s-1')
    group = {}

    # 加载分割文件
    with open(file, 'r', encoding="utf-8")as files:
        file_work = files.read()

    info = info_pattern.findall(file_work)

    name = file_work.split("\n")[1].split(".")[0]
    print(info)

    for body in info:
        mod_name = body[0]
        group[mod_name] = {}
        group[mod_name]['rotate'] = json.loads(body[1])
        group[mod_name]['xy'] = [int(body[2]), int(body[3])]
        group[mod_name]['size'] = [int(body[4]), int(body[5])]

    return name, group


def build_return_list(x, y):
    x = list(x)
    x.extend(list(y))

    return x


def all_file(dir_name, skip_type=r'^UISprite.+$'):
    """
    a function to get all file in a dir
    :param dir_name: the path to get all files
    :param skip_type: the file name pattern which are skipped
    :return: the all files path
    """
    list_keep = os.listdir(dir_name)

    skip_pattern = re.compile(skip_type, flags=re.IGNORECASE)
    out_list = filter(lambda x: os.path.isfile(os.path.join(dir_name, x)) and skip_pattern.match(x) is None,
                      list_keep)
    out_list = map(lambda x: os.path.join(dir_name, x), out_list)

    dir_list = filter(lambda x: os.path.isdir(os.path.join(dir_name, x)), list_keep)
    dir_list = map(lambda x: os.path.join(dir_name, x), dir_list)
    dir_list = map(lambda x: all_file(x, skip_type), dir_list)

    out_list = list(out_list)
    dir_list = list(dir_list)

    return_list = functools.reduce(build_return_list, dir_list, out_list)

    return_list = list(return_list)

    return return_list



def args_got():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-td", "--tex_dir", help="贴图集所在目录", default="./Texture2D", type=str, metavar="tex_dir")
    parser.add_argument("-ad", "--atlas_dir", help="切割文件所在目录", default="./TextAsset", type=str, metavar="atlas_dir")
    parser.add_argument("-tf", "--tex_file", help="单独贴图集文件", type=str, metavar="tex_file")
    parser.add_argument("-af", "--atlas-file", help="单独贴图集文件", type=str, metavar="atlas_file")
    parser.add_argument("-s", "--save_path", help="保存目录，默认为运行目录下out文件夹", default="./out", type=str, metavar="save_path")

    args = parser.parse_args()

    return args


def run(args):
    if args.atlas_file is not None and args.tex_file is not None:
        texture = [args.tex_file]
        atlas = [args.atlas_file]

    elif args.tex_dir is not None and args.atlas_dir is not None:

        texture = all_file(args.tex_dir)
        atlas = all_file(args.atlas_dir)

    else:
        print("没有可用的输入！！")
        return

    texture = list(filter(lambda x: re.match(r'^.+\.png$', x, re.IGNORECASE), texture))
    atlas = list(filter(lambda x: re.match(r'^.+(?:\.atlas|\.atlas\.txt)$', x, re.IGNORECASE), atlas))

    texture_names = list(map(lambda x: os.path.splitext(os.path.splitext(os.path.basename(x))[0])[0], texture))
    atlas_name = list(map(lambda x: os.path.splitext(os.path.splitext(os.path.basename(x))[0])[0], atlas))

    if not (texture_names and atlas_name):
        print("没有可用的输入组合！！")
        return

    count = 1
    for index in range(len(texture_names)):
        try:
            if atlas_name[index] == texture_names[index]:
                name, group = pos_spilt(atlas[index])
                spilt_tex(texture[index], group, name, args.save_path)
                print(f'完成一个，当前第{count}个，为{name}')
                count += 1
        except IndexError:
            continue

    print("完成，将于15s后关闭")

    time.sleep(15)


if __name__ == '__main__':
    args = args_got()
    run(args)

