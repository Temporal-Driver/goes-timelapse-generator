#!/usr/bin/env python
"""
    GOES Timelapse Generator
    Maintained At: https://github.com/Temporal-Driver/goes-timelapse-generator
    This script downloads and assembles satellite data from NOAA's CDN.
"""

import glob
import math
import os.path
from datetime import datetime, timedelta

from PIL import Image
import requests
from bs4 import BeautifulSoup

url = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/'
image_path = os.getcwd() + '\\images'
ssl = True  # I wouldn't change this unless you know what you're doing
hardcode = False  # Uses hardcoded date values to skip the date input sequence
supported_resolutions = [339, 678, 1808, 5424, 10848, 21696]


def main():
    name_loop = True
    running = True
    dates = []
    filename = ''
    resolution = get_resolution()
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    while running:
        while name_loop:
            dates = date_input()
            filename = generate_file_name(dates[0], dates[1])
            if not os.path.exists(os.getcwd() + '\\' + filename):
                name_loop = False
            if os.path.exists(os.getcwd() + '\\' + filename):
                if not hardcode:
                    print('A file has been found containing that timelapse, please pick another range')
                else:
                    name_loop = False
        file_codes = generate_file_codes(dates[0], dates[1])
        results = list_images(file_codes, resolution)
        download_images(results)
        generate_gif(file_codes, filename, resolution)
        print('File created at: ' + image_path + filename + ' | (' \
              + bytes_to_megabytes(os.stat(os.getcwd() + '\\' + filename).st_size) + 'MB)')
        print('-' * 16)
        print('Would you like to create another? (Y/N): ')
        if not yes_no_query():
            running = False
        else:
            main()
    quit()


def get_resolution():
    if hardcode:
        return '1808x1808'
    res_loop = True
    while res_loop:
        valid = False
        while not valid:
            supported_string = ', '.join(str(num) for num in supported_resolutions)
            print('Supported Resolutions - (' + supported_string + ')')
            user_input = int(input('Pick a resolution: '))
            if user_input in supported_resolutions:
                resolution = str(user_input) + 'x' + str(user_input)
                return resolution
            else:
                print('Please enter a supported resolution.')


def date_input():
    date_list = []
    if hardcode:
        date_list.append(datetime.strptime('11-May-2023 09:00', '%d-%b-%Y %H:%M'))
        date_list.append(datetime.strptime('11-May-2023 10:00', '%d-%b-%Y %H:%M'))
        return date_list
    else:
        valid_1 = False
        valid_2 = False
        while not valid_1:
            start = input('Please enter a start date/time (ex. 20-Apr-2023 16:20): ')
            date_start = datetime.strptime(start, '%d-%b-%Y %H:%M')
            if is_valid_date_time(start, '%d-%b-%Y %H:%M'):
                date_list.append(date_start)
                valid_1 = True
            else:
                print('One or both of the dates you entered are invalid!')
        while not valid_2:
            end = input('Please enter an end date/time: ')
            date_end = datetime.strptime(end, '%d-%b-%Y %H:%M')
            if is_valid_date_time(end, '%d-%b-%Y %H:%M'):
                date_list.append(date_end)
                valid_2 = True
            else:
                print('One or both of the dates you entered are invalid!')
        return date_list


def generate_file_name(start, end):
    start_string = start.strftime('%d-%b-%Y %H%M')
    end_string = end.strftime('%d-%b-%Y %H%M')
    name = start_string + ' - ' + end_string + '.gif'
    return name


def generate_gif(file_codes, filename, resolution):
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


def generate_file_codes(d1, d2):
    file_code_list = []
    finished = False
    current_code = d1.strftime('%Y%j%H%M')
    current_time = datetime.strptime(current_code, '%Y%j%H%M')
    file_code_list.append(current_code)
    while not finished:
        added_time = current_time + timedelta(minutes=10)
        file_code_list.append(datetime.strftime(added_time, '%Y%j%H%M'))
        if added_time == d2:
            finished = True
        else:
            current_time = added_time
    return file_code_list


def download_images(results):
    for file in results:
        filename = file.split('//')[-1]
        dl_path = os.path.join(image_path, filename)
        if not os.path.isfile(dl_path):
            r = requests.get(file, allow_redirects=True, verify=ssl)
            open(dl_path, 'wb').write(r.content)


def list_images(valid_codes, resolution):
    def list_files(u=url, e='jpg'):
        page = requests.get(u, verify=ssl).text
        soup = BeautifulSoup(page, 'html.parser')
        return [u + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(e)]

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


# Queries the user and returns either a True (Yes) or False (No) value
def yes_no_query():
    valid = False
    while not valid:
        yes_answer = {'yes', 'y', 'ye', 'hell yes'}
        no_answer = {'no', 'n', 'nah', 'hell no'}
        choice = input().lower()
        if choice in yes_answer:
            return True
        elif choice in no_answer:
            return False
        else:
            print("Please respond with 'yes' or 'no'")


# Takes a string and verifies that it's a valid datetime matching the given format
def is_valid_date_time(date_string, format_string):
    try:
        datetime.strptime(date_string, format_string)
        return True
    except ValueError:
        return False


# Takes a value in bytes and returns it as megabytes rounded to the nearest hundredth
def bytes_to_megabytes(bytes_value):
    megabytes = bytes_value / (1024 * 1024)
    megabytes_string = str(math.floor(megabytes * 100) / 100)
    return megabytes_string


if __name__ == "__main__":
    main()