#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import cv2
import math
import webcolors
import numpy as np

from six import string_types
from tqdm import tqdm
from base64 import b64encode

img_file_ext = ['.png', '.PNG',
                '.jpg', '.JPG', '.jpeg', '.JPEG',
                '.gif', '.GIF']

stdout = getattr(sys.stdout, 'buffer', sys.stdout)


def find_all_files(target_dir):
    for root, dirs, files in os.walk(target_dir):
        for filename in files:
            _filename, extension = os.path.splitext(filename)
            if extension in img_file_ext:
                yield os.path.join(root, filename)


def find_all_files_per_subdir(target, size, keep_aspect, space, space_color, tile_num, limit, imgcat, progress):
    subdir_list = next(os.walk(target))[1]
    for subdir in subdir_list:
        subdirpath = os.path.join(target, subdir)
        output_filename = subdirpath + '.png'
        print("Target:", subdirpath)
        collect(subdirpath, output_filename, False, size, keep_aspect,
                space, space_color, tile_num, limit, imgcat, progress)


def imgcat_for_iTerm2(filename):
    with open(filename, 'rb') as f:
        data = f.read()
        if os.environ['TERM'].startswith('screen'):
            osc = b'\033Ptmux;\033\033]1337;File='
            st = b'\a\033\\\n'
        else:
            osc = b'\033]1337;File='
            st = b'\a\n'
        stdout.write(b'%ssize=%d;inline=1:%s%s' %
                     (osc, len(data), b64encode(data), st))


def create_blank(height, width, rgb_color):
    blank_img = np.zeros((height, width, 3), np.uint8)
    blank_img[:] = tuple(reversed(rgb_color))
    return blank_img


def padding_blank(image, left, top, right, bottom, color):
    height, width = image.shape[:2]
    pad_img = create_blank(height + top + bottom, width + left + right, color)
    pad_img[top:height + top, left:width + left] = image
    return pad_img


def resize_keep_aspect(image, target_width, target_height, color):
    height, width = image.shape[:2]
    height_scale = float(target_height) / height
    width_scale = float(target_width) / width
    resize_scale = min(height_scale, width_scale)

    if (width >= height):
        roi_width = target_width
        roi_height = height * resize_scale
        roi_x = 0
        roi_y = int(math.floor((target_height - roi_height) / 2))
    else:
        roi_y = 0
        roi_height = target_height
        roi_width = width * resize_scale
        roi_x = int(math.floor((target_width - roi_width) / 2))

    roi_width = int(math.floor(roi_width))
    roi_height = int(math.floor(roi_height))

    resized_img = cv2.resize(image, (roi_width, roi_height))
    resized_img = padding_blank(resized_img, roi_x, roi_y, target_width - roi_width - roi_x, target_height - roi_height - roi_y, color)
    return resized_img


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def collect(target, output='output.png', per_subdir=False, size='128x128', keep_aspect=False, space='0', space_color='black', tile_num=0, limit=False, imgcat=False, progress=False):
    filename_list = []
    if (per_subdir):
        print("Create images per subdir. `--output` option is ignored.")
        find_all_files_per_subdir(
            target, size, keep_aspect, space, space_color, tile_num, limit, imgcat, progress)
        return
    else:
        if (os.path.isdir(target)):
            for filename in find_all_files(target):
                filename_list.append(filename)

    if limit:
        limit = int(limit)
        filename_list = filename_list[0:limit]

    print("files:", len(filename_list))
    if (tile_num == 0):
        tile_num = int(math.ceil(math.sqrt(len(filename_list))))
    print("horizontal tile number:", tile_num)

    space = int(space)
    if isinstance(space_color, string_types):
        space_color = webcolors.name_to_rgb(space_color)
    image_list = []
    for filename in tqdm(filename_list, desc='Loading images', disable=(not progress)):
        img = cv2.imread(filename)
        resize_x, resize_y = int(size.split('x')[0]), int(size.split('x')[1])
        if keep_aspect:
            part_img = resize_keep_aspect(img, resize_x, resize_y, space_color)
        else:
            part_img = cv2.resize(img, (resize_x, resize_y))
        if space > 0:
            part_img = padding_blank(part_img, space, space, 0, 0, space_color)
        image_list.append(part_img)

    horizontal_image_list = []
    for horizontal in chunks(image_list, tile_num):
        while (len(horizontal) < tile_num):
            height, width = horizontal[0].shape[:2]
            horizontal.append(create_blank(height, width, space_color))
        horizontal_image_list.append(cv2.hconcat(horizontal))

    result_img = cv2.vconcat(horizontal_image_list)

    if space > 0:
        result_img = padding_blank(result_img, 0, 0, space, space, space_color)

    stdout.write(b'Saving... ')
    stdout.flush()
    cv2.imwrite(output, result_img)
    stdout.write(b'\rSaved: %s\n' % output.encode('utf8'))

    if imgcat:
        imgcat_for_iTerm2(output)


if __name__ == '__main__':
    import fire
    fire.Fire(collect)
