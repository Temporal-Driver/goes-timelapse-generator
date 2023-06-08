#!/usr/bin/env python
"""
    GOES Timelapse Generator
    Maintained At: https://github.com/Temporal-Driver/goes-timelapse-generator
    This script downloads and assembles satellite data from NOAA's CDN.
"""

import argparse
import glob
import json
import math
import os
from datetime import datetime, timedelta

from modules import image_handling
from modules import command_parser

version = '0.2.2'

image_path = os.getcwd() + '/images'
preset_path = os.getcwd() + '/presets.json'
with open(preset_path) as file:
    preset_data = json.load(file)
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
    pretty_dates = []
    for d in [args.start, args.end]:
        pretty_dates.append(datetime.strftime(datetime.strptime(d, '%d-%b-%Y %H:%M'), '%d %b %Y at %H:%M'))
    divider = '----------------------------------------'
    print(divider)
    print(f'GOES Timelapse Generator - Version {version}')
    print(divider)
    for index, arg in enumerate(pretty_dates):
        if index == 0:
            print('   Start Date: ' + pretty_dates[index])
        else:
            print('   End Date: ' + pretty_dates[index])
    print(divider)
    start = datetime.strptime(args.start, '%d-%b-%Y %H:%M')
    end = datetime.strptime(args.end, '%d-%b-%Y %H:%M')
    filename = generate_file_name(start, end)
    url = build_url(args.sat, args.region, args.band)
    resolution = sizes[args.size][0 if args.region == 'disk' else 1]
    file_codes = generate_file_codes(start, end, args.region)
    results = image_handling.list_images(file_codes, resolution, url)
    if len(results) == 0:
        print('No photos found for ' + args.start + ' through ' + args.end + '.')
        quit()
    else:
        print('Found (' + str(len(results)) + ') photos for ' + args.start + ' through ' + args.end + '.')
    image_handling.download_images(results, image_path, ssl)
    files_used = image_handling.generate_gif(file_codes, filename, resolution, image_path)
    if os.path.isfile(os.getcwd() + '/' + filename):
        size = bytes_to_megabytes(os.path.getsize(os.getcwd() + '/' + filename))
        print('Success! Filename: ' + filename + ' | File Size: ' + size + 'MB')
        # delete images if --keep is not used
        if not args.keep:
            deleted_total = 0
            for pics in glob.glob(image_path + '/*.jpg'):
                if pics in files_used:
                    deleted_total += os.path.getsize(pics)
                    os.remove(pics)
            print('Deleted ' + bytes_to_megabytes(deleted_total) + 'MB from /images/ folder.')
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


def arg_manager(parser):
    def validate_date_format(date_string):
        try:
            datetime.strptime(date_string, '%d-%b-%Y %H:%M')
            return date_string
        except ValueError:
            return None

    # Returns None if the value is not an integer. Used for checking --end
    def try_int(v):
        try:
            result = int(v)
            return result
        except ValueError:
            return None

    # If --preset is passed
    if args.preset:
        if args.preset not in preset_data.keys():
            parser.error(f"Invalid preset '{args.preset}'. Valid presets: {', '.join(preset_data.keys())}")
        preset = preset_data[args.preset]
        missing_args = []
        if args.size is None:
            args.size = 'medium'
        # check if any necessary args are missing from the preset and command
        for arg_name in ['sat', 'region', 'start', 'end']:
            preset_value = preset.get(arg_name)
            arg_value = getattr(args, arg_name)
            if not preset_value and arg_value is None:
                missing_args.append(arg_name)
        if missing_args:
            parser.error(f"These arguments are required for '{args.preset}': {', '.join(missing_args)}")
        # override any inputs with the preset values if they are not empty
        for arg_name in ['sat', 'region', 'size', 'start', 'end']:
            preset_value = preset.get(arg_name)
            if not preset_value == '':
                setattr(args, arg_name, preset.get(arg_name).lower())
    # If no preset is passed, any missing arguments throw an error
    if args.preset is None:
        if args.sat is None or args.region is None or args.start is None or args.end is None:
            parser.error('If --preset is not specified, all other arguments are required.')
    # Verifying date arguments, accounting for tags like "now" and "+x/-x"
    if not args.start.lower() == 'now' and not validate_date_format(args.start):
        parser.error(command_parser.start_date_error)
    if try_int(args.end) is None and not validate_date_format(args.end):
        parser.error(command_parser.end_date_error)
    if args.start.lower() == 'now':
        args.start = datetime.utcnow().strftime('%d-%b-%Y %H:%M')
    if try_int(args.end) is not None:
        old_time = datetime.strptime(args.start, '%d-%b-%Y %H:%M')
        new_time = old_time + timedelta(hours=int(args.end))
        args.end = new_time.strftime('%d-%b-%Y %H:%M')
        if datetime.strptime(args.start, '%d-%b-%Y %H:%M') > datetime.strptime(args.end, '%d-%b-%Y %H:%M'):
            t = args.start
            args.start = args.end
            args.end = t
    else:
        if datetime.strptime(args.start, '%d-%b-%Y %H:%M') > datetime.strptime(args.end, '%d-%b-%Y %H:%M'):
            parser.error('Start date must be before end date. (Unless using --end +x/-x)')


if __name__ == '__main__':
    cmd_parser = argparse.ArgumentParser(description='GOES Timelapse Generator')
    command_parser.arg_setup(cmd_parser)
    args = cmd_parser.parse_args()
    arg_manager(cmd_parser)
    main()
