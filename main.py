#!/usr/bin/env python
"""
    GOES Timelapse Generator
    Maintained At: https://github.com/Temporal-Driver/goes-timelapse-generator
    This script downloads and assembles satellite data from NOAA's CDN.
"""

import math
import os
from datetime import datetime, timedelta

from modules import input_tools
from modules import image_handling

image_path = os.getcwd() + '/images'
ssl = True  # I wouldn't change this unless you know what you're doing


def main():
    name_loop = True
    running = True
    dates = []
    filename = ''
    url = input_tools.pick_satellite()
    supported_resolutions = image_handling.parse_resolution(url)
    resolution = input_tools.get_resolution(supported_resolutions)
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    while running:
        while name_loop:
            dates = input_tools.date_input()
            filename = generate_file_name(dates[0], dates[1])
            if not os.path.exists(os.getcwd() + '/' + filename):
                name_loop = False
            if os.path.exists(os.getcwd() + '/' + filename):
                print('A file with that range was found, please pick another')
            else:
                name_loop = False
        file_codes = generate_file_codes(dates[0], dates[1])
        results = image_handling.list_images(file_codes, resolution, url, ssl)
        image_handling.download_images(results, image_path, ssl)
        image_handling.generate_gif(file_codes, filename, resolution, image_path)
        print('File created at: ' + image_path + filename + ' | ('
              + bytes_to_megabytes(os.stat(os.getcwd() + '/' + filename).st_size) + 'MB)')
        print('-' * 16)
        print('Would you like to create another? (Y/N): ')
        if not input_tools.yes_no_query():
            running = False
        else:
            main()
    quit()


# Takes a start and end datetime object and generates a filename
def generate_file_name(start, end):
    start_string = start.strftime('%d-%b-%Y %H%M')
    end_string = end.strftime('%d-%b-%Y %H%M')
    name = start_string + ' - ' + end_string + '.gif'
    return name


# Generates a list of 'file codes' for use in the search (Format: YYYYDDDHHMM)
# YYYY = Year  |  DDD = Day of Year  |  HH = Hour  |  MM = Minute
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


# Takes a value in bytes and returns it as megabytes rounded to the nearest hundredth
def bytes_to_megabytes(bytes_value):
    megabytes = bytes_value / (1024 * 1024)
    megabytes_string = str(math.floor(megabytes * 100) / 100)
    return megabytes_string


if __name__ == "__main__":
    main()
