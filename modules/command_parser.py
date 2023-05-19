from datetime import datetime


class CaseInsensitive:
    def __call__(self, value):
        return value.lower()


def process_args(parser):
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
        help='Pick the start date and time in quotes (Example: 12-May-2023 15:20)'
    )
    parser.add_argument(
        '--end',
        type=str,
        help='Pick the end date and time in quotes (Example: 12-May-2023 15:20)'
    )
