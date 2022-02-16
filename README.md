# ROI Motion detection utility

This is simple motion detection filter that allow to proccess video files and detect motion in provided ROI

Process is split into two phases.

Detection phases and navigation phase. 

On the first stage 'motion_detection' utility detect ROI motions and save frame metrics into csv files.

On the second stage 'motion_preview' utility allow to check all detections across proccessed files and make a video preview via 'ffplay' by **clicking** on detection bars

![Screenshot from 2022-02-16 05-02-38](https://user-images.githubusercontent.com/4415914/154182659-813a2d3c-49df-4bbc-8986-f6443fbaae0f.png)

![Screenshot from 2022-02-16 04-58-21](https://user-images.githubusercontent.com/4415914/154181780-fd1b33a4-d932-4fa2-9076-ec92bca1e284.png)

![Screenshot from 2022-02-16 04-54-53](https://user-images.githubusercontent.com/4415914/154181647-37c1a3fd-396f-4c0c-8bfc-1941554baf7a.png)

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
