"""
input_tools.py

This module provides a set of functions for handling user input.

Used In: goes-timelapse-generator
http://github.com/Temporal-Driver/goes-timelapse-generator

Functions:
- get_resolution(supported_resolutions): Prompts user for a supported resolution and returns it formatted for use.
- yes_no_query(): Prompts the user to enter a valid yes or no answer and returns True or False.
- date_input(): Prompts user for start & end date/time & returns them as datetime objects.

"""

from datetime import datetime


# Prompts the user to enter a valid yes or no answer and returns True or False
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


# Prompts the user for a supported resolution and returns it formatted for use
# Pass a list of supported resolutions
def get_resolution(supported_resolutions):
    resolution_strings = list(map(str, supported_resolutions))
    supported_string = ', '.join(res for res in resolution_strings)
    while 1 != 2:
        print('Supported Resolutions - (' + supported_string + ')')
        user_input = input('Pick a resolution: ')
        user_input = str(user_input) if user_input.isdigit() else user_input
        if user_input in resolution_strings:
            resolution = str(user_input) + 'x' + str(user_input)
            return resolution
        else:
            print('Please enter a supported resolution.')


def pick_satellite():
    print('Please pick a satellite:')
    print('1. GOES-East  |  2. GOES-West')
    while 1 != 2:
        user_input = input()
        if str(user_input) == '1':
            url = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/'
            return url
        if str(user_input) == '2':
            url = 'https://cdn.star.nesdis.noaa.gov/GOES18/ABI/FD/GEOCOLOR/'
            return url
        else:
            print('Please enter a valid choice.')


def date_input():
    # Takes a string and verifies that it's a valid datetime matching the given format
    def is_valid_date_time(date_string, date_format):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    date_list = [None] * 2
    valid = False
    for i in range(2):
        if i == 0:
            print('Please enter a start date/time (ex. 20-Apr-2023 16:20): ')
        elif i == 1:
            print('Please enter an end date/time: ')
        while True:
            date_in = input()
            if is_valid_date_time(date_in, '%d-%b-%Y %H:%M'):
                date_list[i] = datetime.strptime(date_in, '%d-%b-%Y %H:%M')
                break
            else:
                print('Please enter a valid date/time.')
    return date_list
