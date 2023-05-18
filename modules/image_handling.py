"""
image_handling.py

This module provides a set of functions for handling image downloads.

Functions:
    download_images(results, image_path, ssl)
    list_files(url, ext='jpg')
    list_images(valid_codes, resolution, url, ssl)
    generate_gif(file_codes, filename, resolution, image_path)

"""
import glob
import os
from PIL import Image
import requests
from bs4 import BeautifulSoup


# import itertools
# import re


# downloads images from a list of urls
def download_images(results, image_path, ssl):
    for file in results:
        filename = file.split('//')[-1]
        dl_path = os.path.join(image_path, filename)
        if not os.path.isfile(dl_path):
            r = requests.get(file, verify=ssl)
            open(dl_path, 'wb').write(r.content)


# lists all files in a given CDN directory
def list_files(u, e='jpg'):
    page = requests.get(u).text
    soup = BeautifulSoup(page, 'html.parser')
    return [u + '/' + node.get('href') for node in
            soup.find_all('a') if node.get('href').endswith(e)]


# takes file codes and resolutions and returns matching files
def list_images(valid_codes, resolution, url, ssl):
    filtered = []
    result_list = []
    for file in list_files(url):
        if resolution in file:
            result_list.append(file)
    for file in result_list:
        for res in valid_codes:
            if res in file:
                filtered.append(file)
    return filtered


# generates a gif using all images that match
# I'd eventually like to make this smarter now that command arguments exist
# but for now it works and I don't want to break it
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
