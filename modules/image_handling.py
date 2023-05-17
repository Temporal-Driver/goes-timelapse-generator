"""
image_handling.py

This module provides a set of functions for handling image downloads.

Used In: goes-timelapse-generator
http://github.com/Temporal-Driver/goes-timelapse-generator

"""
import glob
import os
from PIL import Image
import requests
from bs4 import BeautifulSoup
import itertools
import re


def download_images(results, image_path, ssl):
    for file in results:
        filename = file.split('//')[-1]
        dl_path = os.path.join(image_path, filename)
        if not os.path.isfile(dl_path):
            r = requests.get(file, verify=ssl)
            open(dl_path, 'wb').write(r.content)


def list_files(u, e='jpg'):
    page = requests.get(u).text
    soup = BeautifulSoup(page, 'html.parser')
    return [u + '/' + node.get('href') for node in
            soup.find_all('a') if node.get('href').endswith(e)]


# finds available resolutions by taking the last 15 characters of a sample of file names
def parse_resolution(url):
    sample_list = list(itertools.islice(list_files(url, 'jpg'), 20))
    cut_list = []
    for item in sample_list:
        cut_list.append(item[-15:])
    pattern = r'x\d+'  # regex pattern to find digits after an x
    resolutions = []
    for string in cut_list:
        match = re.findall(pattern, string)[0][1:]
        if match not in resolutions:
            resolutions.append(match)
    resolution_list = [int(i) for i in resolutions]
    resolution_list.sort()
    sample_list.clear()
    return resolution_list  # returns a list of resolutions as integers


def list_images(valid_codes, resolution, url, ssl):
    filtered = []
    result_list = []
    for file in list_files():
        if resolution in file:
            result_list.append(file)
    for file in result_list:
        for res in valid_codes:
            if res in file:
                filtered.append(file)
    return filtered


def generate_gif(file_codes, filename, resolution, image_path):
    image_frames = [None] * len(file_codes)
    images_in_folder = glob.glob(image_path + '/*.jpg')
    for img_path in images_in_folder:
        for i, code in enumerate(file_codes):
            if code in img_path and resolution in img_path:
                image_frames[i] = Image.open(img_path)
    image_frames[0].save(filename, format='GIF',
                         append_images=image_frames[1:],
                         save_all=True,
                         duration=1, loop=0)
