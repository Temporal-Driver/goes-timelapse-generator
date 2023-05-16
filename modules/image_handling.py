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


# TODO: Figure out issue printing new lines
def download_images(results, image_path, ssl, return_paths=False):
    file_paths = []
    for file in results:
        filename = file.split('//')[-1]
        file_paths.append(os.path.join(image_path, filename))
        dl_path = os.path.join(image_path, filename)
        if not os.path.isfile(dl_path):
            print('\rDownloading: ' + filename)
            r = requests.get(file, allow_redirects=True, verify=ssl)
            open(dl_path, 'wb').write(r.content)
        else:
            print('\rFile Found (Skipping): ' + filename)
    if return_paths:
        return file_paths


def list_images(valid_codes, resolution, url, ssl):
    def list_files(u=url, e='jpg'):
        page = requests.get(u, verify=ssl).text
        soup = BeautifulSoup(page, 'html.parser')
        return [u + '/' + node.get('href') for node in
                soup.find_all('a') if node.get('href').endswith(e)]

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
    image_frames = []
    images_in_folder = glob.glob(image_path + '\\*.jpg')
    for img_path in images_in_folder:
        for code in file_codes:
            if code in img_path and resolution in img_path:
                new_frame = Image.open(img_path)
                image_frames.append(new_frame)
    image_frames[0].save(filename, format='GIF',
                         append_images=image_frames[1:],
                         save_all=True,
                         duration=1, loop=0)
