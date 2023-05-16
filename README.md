# GOES Timelapse Generator
#### A simple Python script to generate timelapses from images found at NOAA's [CDN](https://cdn.star.nesdis.noaa.gov/GOES16/)

Heavily W.I.P, and I've never maintained a GitHub repo before, so if you have any questions or suggestions feel free to contact me.
___
### Features

- GOES-East Full Disk GIF Timelapses
- GOES-West Full Disk GIF Timelapses
___
### Planned Features
- More regions than just Full Disk
- Saving presets
- GIF compression
- FFMPEG functionality to generate videos
- Smarter user experience (i.e. command line usage rather than input prompts)
---
## How To Use
- Clone the repo or download a release
- Install the required libraries from requirements.txt  
*(Open your shell in the repo/release folder)*
```shell
pip install -r requirements.txt
```
- Run main.py and follow the instructions
#### Note:
- When you enter a start/end time, make sure the minutes are in increments of 10 otherwise no images will be found. (This will be fixed in a future update)
- Times are in UTC
- Images are not yet deleted automatically, so be sure to clear out the images folder to save space after generating.
___
### Authors

- [@Temporal-Driver](https://www.github.com/temporal-driver)