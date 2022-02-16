import os, sys
import argparse
import logging
import json
import random
import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageColor, ImageTk
import io
import cv2
import pandas as pd
import glob

import ffmpeg
import ffplayer

test_video="/home/er/workspace/md_filter/10.0.6.25_04_20220212124853446.mp4"
test_markup = "/home/er/workspace/md_filter/out/10.0.6.25_04_20220212124853446.mp4.[1690,0,220,220].csv"


def get_img_data(img, first=False):
    
    if img.shape[0] > 960:
        scale = 960 / img.shape[0] 
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        dim = (width, height)

        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

def create_bar(w, h, df):
    motion_vals = (df["motion"] > 0.001).astype('uint8')
    
    hist, acc_hist = np.histogram(df.index, bins=bar_width, weights=motion_vals)
    hist = hist / np.max(hist) 

    bar_r = np.tile(hist, (bar_height, 1))
    bar_g = np.tile(1.0 - hist, (bar_height, 1))
    bar_b = np.zeros((bar_height, bar_width), dtype=np.float)

    motion_bar_img = (cv2.merge((bar_b, bar_g, bar_r)) * 255).astype(np.uint8)

    return motion_bar_img

parser = argparse.ArgumentParser(description='Motion detection preview')
parser.add_argument("--src", metavar="FOLDER", default='.', help="Path to source videos")
parser.add_argument("--detections", metavar="FOLDER", default='./out1', help="Path to folder with detection csv")

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

csv_files = glob.glob(os.path.join(args.detections, "*.csv"))

bar_height, bar_width = 20, 1000

layout = []
for n, csv_file in enumerate(csv_files, start=0):
    
    csv_name = os.path.basename(csv_file)

    # parse video file 
    video_name, _ = csv_name.split('.mp4')
    video_file = os.path.abspath(os.path.join(args.src, f"{video_name}.mp4"))

    probe = ffmpeg.probe(video_file)

    # print("probe:", probe)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    fps = int(video_info['r_frame_rate'].split('/')[0])
    duration = float(video_info['duration'])

    df = pd.read_csv(csv_file)

    print("fps:", fps, "duration:", duration, "df_shape:", df.shape)

    meta = {'file' : video_file, 'duration': duration, 'markup' : df}
    text = f'File: {video_file}\nDuration: {ffplayer.duratioin_format(duration)}'

    layout.append([sg.Text(text, key=f'-FILE_TEXT_{n}-')])
    layout.append([sg.Graph((bar_width, bar_height), (0, bar_height), (bar_width, 0), change_submits=True, key=f'-MOTION_BAR_{n}-', enable_events=True, metadata=meta)])

# Add scrollbar if more that 10 clips
if len(csv_files) > 2:
    layout = [[sg.Column(layout, scrollable=True,  vertical_scroll_only=True)]]

window = sg.Window(f'Motion detection preview {args.src}', layout, return_keyboard_events=True).Finalize()

for n in range(len(csv_files)):
    el = window[f"-MOTION_BAR_{n}-"]
    df = el.metadata['markup']

    el.draw_image(data=get_img_data(create_bar(bar_width, bar_height, df), first=True), location=(0,0))

# player
player = ffplayer.FFPlayer()

while True:  # Event Loop
    event, values = window.read()
    
    if event and "MOTION_BAR" in event:
        el = window[event]
        bar_pos, _ = values[event]

        ts = bar_pos / bar_width * el.metadata["duration"]
        
        player.run_player(el.metadata["file"], ts)

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
