class CaseInsensitive:
    def __call__(self, value):
        return value.lower()


# I'm keeping this here because it makes main.py look ugly
end_date_error = 'Invalid end format. Use a date in quotes: "14-May-2023 16:20" or use -x/+x to add/remove hours.'
start_date_error = 'Invalid start format. Use a date in quotes: "14-May-2023 16:20", or --start now'


def arg_setup(parser):
    from main import preset_data
    parser.add_argument(
        '--preset',
        type=CaseInsensitive(),
        choices=preset_data.keys(),
        help='Pick a preset name'
    )
    parser.add_argument(
        '-s', '--sat',
        type=CaseInsensitive(),
        choices=['east', 'west'],
        help='Specify which satellite (GOES-East or GOES-West)'
    )
    parser.add_argument(
        '-r', '--region',
        type=CaseInsensitive(),
        choices=['disk', 'conus'],
        help='Specify which region (Full Disk or Continental US)'
    )
    parser.add_argument(
        '--size',
        type=CaseInsensitive(),
        default='medium',
        choices=['small', 'medium', 'large',
                 'full', 'max'],
        help='Specify what size images to download (Medium is default)'
    )
    parser.add_argument(
        '--start',
        type=str,
        help='Pick the start date and time in quotes (Example: "14-May-2023 16:20"), or use --start now'
    )
    parser.add_argument(
        '--end',
        type=str,
        help='Pick the end date and time in quotes (Example: "14-May-2023 16:20"), or use -x/+x to add/remove hours'
    )
