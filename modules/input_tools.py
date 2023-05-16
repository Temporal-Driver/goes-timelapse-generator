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
    # Takes a string and verifies that it's a valid datetime matching the given format
    def is_valid_date_time(date_string, format_string):
        try:
            datetime.strptime(date_string, format_string)
            return True
        except ValueError:
            return False

    date_list = []
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
