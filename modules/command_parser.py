from datetime import datetime

sizes = {
    'small': ['678x678', '625x375'],
    'medium': ['1808x1808', '1250x750'],
    'large': ['5424x5424', '5000x3000'],
    'full': ['10848x10848', '10000x6000'],
    'max': ['21696x21696', '10000x6000']
}


class CaseInsensitive:
    def __call__(self, value):
        return value.lower()


def validate_date_format(cmd_parse, date_string):
    try:
        datetime.strptime(date_string, '%d-%b-%Y %H:%M')
        return date_string
    except ValueError:
        cmd_parse.error('Invalid date format. Example: "12-May-2023 15:20"')


def process_args(parser):
    required_choices = parser.add_argument_group('Required Arguments')
    required_choices.add_argument(
        '-f', '--format',
        type=CaseInsensitive(),
        choices=['gif', 'mp4'],
        required=True,
        help='Choose the format to generate your timelapse (.GIF or .MP4)'
    )
    required_choices.add_argument(
        '-s', '--sat',
        type=CaseInsensitive(),
        choices=['east', 'west'],
        required=True,
        help='Specify which satellite (GOES-East or GOES-West)'
    )
    required_choices.add_argument(
        '-r', '--region',
        type=CaseInsensitive(),
        choices=['disk', 'conus'],
        required=True,
        help='Specify which region (Full Disk or Continental US)'
    )
    # parser.add_argument(
    #     '-b', '--band',
    #     type=CaseInsensitive(),
    #     default='geocolor',
    #     choices=['airmass', 'daycloudphase', 'dust',
    #              'firetemperature', 'geocolor', 'sandwich'],
    #     help='Specify which band (GEOCOLOR is default)'
    # )
    parser.add_argument(
        '--size',
        type=CaseInsensitive(),
        default='medium',
        choices=['small', 'medium', 'large',
                 'full', 'max'],
        help='Specify what size images to download (Medium is default)'
    )
    required_choices.add_argument(
        '--start',
        type=lambda start: validate_date_format(parser, start),
        required=True,
        help='Pick the start date and time in quotes (Example: 12-May-2023 15:20)'
    )
    required_choices.add_argument(
        '--end',
        type=lambda end: validate_date_format(parser, end),
        required=True,
        help='Pick the end date and time in quotes (Example: 12-May-2023 15:20)'
    )
