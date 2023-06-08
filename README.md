

# GOES Timelapse Generator  
  
#### A simple Python script to generate timelapses from images found at NOAA's [CDN](https://cdn.star.nesdis.noaa.gov/GOES16/)  
  
This is my first time trying to make more than just a prototype in Python, and my first time using GitHub, so you may see problems here and there. Let me know and I'll do my best to fix them.  
___  
  
### Features  
  
- GOES Full Disk / CONUS Timelapses
- Different bands (GEOCOLOR, Fire Temperature, etc.)
- Save presets for quick generation
![Full Disk Example](https://raw.githubusercontent.com/secondbyte/gtg-images/main/Full%20Disk%20Example.png)![Full Disk Example](https://raw.githubusercontent.com/secondbyte/gtg-images/main/CONUS%20Example.png)
___  
  
### Planned Features
- File size estimation
- GIF compression  
- FFMPEG functionality to generate videos  
- Batch generation  
  
## Usage  
  
1. Clone the repo or download a release  
2. Navigate via command-line to the goes-timelapse-generator folder  
3. Install the required libraries from requirements.txt  
  
```shell  
pip install -r requirements.txt
```  
  
4. Run main.py with your desired settings  
  
```shell  
See examples below
```  
  
| Flags | Arguments (Case-Insensitive) |  
|------------------|-----------------------------------------------------------------------------------------------------------------|  
| `--preset` | Takes names from presets.json, such as `--preset last_12_west_disk` |
| `-s`, `--sat` | Accepts `East` for GOES-16 or `West` for GOES-18 |  
| `-r`, `--region` | Accepts `CONUS` for Continental U.S., or `Disk` for the Full Disk image |  
| `--size` | Accepts `Small` , `Medium` , `Large` , `Full` , or `Max`  *Optional: Defaults to Medium* |  
| `--start` | Start date/time in quotes (UTC 24-hour Clock) Ex: `"12-May-2023 16:20"` or use `--start now` |  
| `--end` | End date/time in quotes *(Same formatting as above)* Or `+x`/`-x` to add or subtract that many hours from the start time |  
| `--keep` | Prevents deleting source images after generating the timelapse |
  
## Examples  
  
- Generate a timelapse of GOES-East's CONUS view:  
  
```shell  
$ python main.py --sat east --region conus --start "12-May-2023 12:00" --end "12-May-2023 22:00"
```  
  
- Generate a large sized timelapse of GOES-West's Full Disk view:  
  
```shell  
$ python main.py -s west -r disk --size large --start "13-May-2023 14:00" --end "13-May-2023 20:00"
```  
  
- Run the program with a full preset:  
  
```shell  
$ python main.py --preset last_12_west_disk
```  
- Run the program with a preset missing variables:  
  
```shell  
$ python main.py --preset east_disk_large --start now --end -5
``` 
- Run the program with a preset and don't delete downloaded files:  
  
```shell  
$ python main.py --preset last_12_west_disk --keep
``` 
  
___  
  
### Authors  
  
- [@Temporal-Driver](https://www.github.com/temporal-driver)
