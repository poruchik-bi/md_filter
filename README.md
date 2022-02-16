# Motion detection utility

This is simple motion detection filter that allow to proccess video files and detect motion in provided ROI

Process is split into two phases.
Detection phases and navigation phase. 
On the first stage 'motion_detection' utility detect ROI motions and save frame metrics into csv files.
On the second stage 'motion_preview' utility allow to check all detections across proccessed files and make a video preview via 'fflay'

### Dependency

```
pip3 install Pillow ffmpeg-python pysimplegui pandas python-opencv logging
pip3 install pyinstaller
```

Make binary 
```
pyinstaller --paths=. --onefile .\motion_detection.py
pyinstaller --paths=. --onefile .\motion_preview.py
```

### Usage

```
cd <folder-with-video>
<path-to>/motion_detection
<path-to>/motion_preview
```

```
usage: motion_detection.py [-h] [-i FOLDER] [-o FOLDER] [-r ROI] [-g GAIN] [--show] [--ext EXT]

ROI motion detection

optional arguments:
  -h, --help            show this help message and exit
  -i FOLDER, --in FOLDER
                        Source video folder (default: .)
  -o FOLDER, --out FOLDER
                        Result folder (default: out)
  -r ROI, --roi ROI     ROI [x,y,w,h] (default: [1690, 0, 220, 220])
  -g GAIN, --gain GAIN  Gain (0 .. 1) (default: 0.5)
  --show                Show video (default: False)
  --ext EXT             Video files extension (default: mp4)

```

```
usage: motion_preview.py [-h] [--src FOLDER] [--detections FOLDER]

Motion detection preview

optional arguments:
  -h, --help           show this help message and exit
  --src FOLDER         Path to source videos (default: .)
  --detections FOLDER  Path to folder with detection csv (default: out)
```


Tested on 
   - Ubuntu 21.10 
   - Windows 10
### Contacts

poruchik_bI@gmail.com
