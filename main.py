#!/usr/bin/env python
"""
    GOES Timelapse Generator
    Maintained At: https://github.com/Temporal-Driver/goes-timelapse-generator
    This script downloads and assembles satellite data from NOAA's CDN.
"""
__version__ = '0.2.0'

import argparse
import math
import os
from datetime import datetime, timedelta

from modules import image_handling
from modules import command_parser

image_path = os.getcwd() + '/images'
os.makedirs(image_path, exist_ok=True)
ssl = True  # I keep this here because ssl expired while testing, in case it happens again

sizes = {  # [   disk  ,    conus   ]
    'small': ['678x678', '625x375'],
    'medium': ['1808x1808', '1250x750'],
    'large': ['5424x5424', '5000x3000'],
    'full': ['10848x10848', '10000x6000'],
    'max': ['21696x21696', '10000x6000']
}


def main():
    args.band = 'geocolor'
    start = datetime.strptime(args.start, '%d-%b-%Y %H:%M')
    end = datetime.strptime(args.end, '%d-%b-%Y %H:%M')
    filename = generate_file_name(start, end)
    url = build_url(args.sat, args.region, args.band)
    resolution = sizes[args.size][0] if args.region == 'disk' else sizes[args.size][1]
    file_codes = generate_file_codes(start, end, args.region)
    results = image_handling.list_images(file_codes, resolution, url)
    image_handling.download_images(results, image_path, ssl)
    image_handling.generate_gif(file_codes, filename, resolution, image_path)
    quit()


# generates an output filename based on the start and end times
# appends a number to the end if the filename already exists
def generate_file_name(d1, d2):
    date_string_1 = datetime.strftime(d1, '%d-%m-%y %H%M')
    date_string_2 = datetime.strftime(d2, '%d-%m-%y %H%M')
    filename = date_string_1 + ' - ' + date_string_2 + '.gif'
    if os.path.isfile(os.getcwd() + '/' + filename):
        name_taken = True
        attempt = 1
        while name_taken:
            new_filename = filename.split('.')[0] + ' (' + str(attempt) + ').gif'
            if os.path.isfile(os.getcwd() + '/' + new_filename):
                attempt += 1
            else:
                return new_filename
    else:
        return filename


# generates a list of valid file codes between the given start and end times
# conus: 5 minute intervals on 1s and 6s  |  disk: 10 minute intervals
# I'd eventually like to make this more dynamic in case they change intervals
def generate_file_codes(d1, d2, region):
    def round_to_interval(num_in):
        values = []
        if region == 'disk':
            values = [0, 10, 20, 30, 40, 50]
        elif region == 'conus':
            values = [6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56]
        closest = min(values, key=lambda x: abs(x - num_in))
        return closest

    times = [d1.minute, d2.minute]
    for time in times:
        rounded = round_to_interval(time)
        times[times.index(time)] = rounded
    d1 = d1.replace(minute=times[0])
    d2 = d2.replace(minute=times[1])
    file_code_list = []
    current_code = d1.strftime('%Y%j%H%M')
    current_time = datetime.strptime(current_code, '%Y%j%H%M')
    file_code_list.append(current_code)
    while True:
        min_to_add = 10 if region == 'disk' else 5
        added_time = current_time + timedelta(minutes=min_to_add)
        file_code_list.append(datetime.strftime(added_time, '%Y%j%H%M'))
        if added_time == d2:
            return file_code_list
        else:
            current_time = added_time


# Takes a satellite, region, and band and returns the CDN URL
def build_url(sat, region, band):
    band_mapping = {
        'airmass': 'AirMass/',
        'daycloudphase': 'DayCloudPhase/',
        'dust': 'Dust/',
        'firetemperature': 'FireTemperature/',
        'geocolor': 'GEOCOLOR/',
        'sandwich': 'Sandwich/'
    }
    url = 'https://cdn.star.nesdis.noaa.gov/{sat}/{region}/{band}'.format(
        sat='GOES16/ABI' if sat == 'east' else 'GOES18/ABI',
        region='FD' if region == 'disk' else 'CONUS',
        band=band_mapping.get(band, '')
    )
    return url


# Takes a value in bytes and returns it as megabytes rounded to the nearest hundredth
def bytes_to_megabytes(bytes_value):
    megabytes = bytes_value / (1024 * 1024)
    megabytes_string = str(math.floor(megabytes * 100) / 100)
    return megabytes_string


if __name__ == '__main__':
    cmd_parser = argparse.ArgumentParser(description='GOES Timelapse Generator')
    command_parser.process_args(cmd_parser)
    args = cmd_parser.parse_args()
    main()
