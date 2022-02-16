
from cgitb import lookup
import os, sys
import cv2
import argparse
import logging
import pandas as pd
import numpy as np
import altair as alt
from altair import datum

alt.renderers.enable('mimetype')


test_video="/home/er/workspace/md_filter/10.0.6.25_04_20220212124853446.mp4"
test_roi = [2*845,0,2*110,2*110]

if __name__ == "__main__":

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                        level=LOGLEVEL,
                        datefmt="%Y-%m-%d %H:%M:%S")

    parser = argparse.ArgumentParser(description='ROI motion detection')
    parser.add_argument("-i", "--in", default = [test_video], dest = 'input', nargs='+', metavar="VIDEO", help="Source videos")
    parser.add_argument("-o", "--out", default='out', metavar="FOLDER", help='Result folder')
    parser.add_argument("-r", "--roi", default=test_roi, metavar="ROI", help='ROI [x,y,w,h]')
    parser.add_argument("-g", "--gain", default=0.5, type=float, metavar="GAIN", help='Gain (0 .. 1)')
    parser.add_argument("--show", default=False, action='store_true', help='Show video')

    args = parser.parse_args()
    
    os.system(f'mkdir -p {args.out}')

    alpha = 1 - args.gain
    
    motion_hist = [0]
    
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    x,y,w,h = args.roi
    for path in args.input:
        
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        diff_path = os.path.join(args.out,os.path.basename(path))
        # writer = cv2.VideoWriter(diff_path, fourcc, fps, (int(w/2), int(h/2)))

        logging.info(f"Video fps: {fps} path: {path}")

        ret = True
        frame0 = None
        comm_diff = None 
        
        frame_id = 0
        while ret:
            
            ret, frame_orig = cap.read()
            if ret == True:
                
                # frame_orig = cv2.pyrDown(frame_orig)
                frame = frame_orig[y:y+h, x:x+w]
                frame = cv2.pyrDown(frame)

                if frame0 is not None:
                    frame = cv2.medianBlur(frame, 5)

                    diff = cv2.absdiff(frame0, frame)
                    
                    b,g,r = cv2.split(diff)
                    diff = cv2.max(cv2.max(b,g),r)

                    diff_ad = cv2.adaptiveThreshold(diff, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 7)
                    # diff[diff < 10] = 0
                    
                    comm_diff = diff if comm_diff is None else (alpha * comm_diff + (1-alpha) * diff).astype(np.uint8)

                    if args.show:
                        frame_orig = cv2.rectangle(frame_orig, args.roi, (0, 0, 255), 2) 
                        cv2.imshow('Frame', cv2.pyrDown(frame_orig))
                        cv2.imshow('Diff', comm_diff.astype(np.uint8))
                        cv2.imshow('Diff ad', diff_ad.astype(np.uint8))
                    
                    motion = (np.sum(diff_ad) / diff_ad.size / 255)
                    motion_hist.append(motion)
                    # logging.info(f"ROI sum: {motion}")
                
                    diff_dst = cv2.cvtColor(comm_diff, cv2.COLOR_GRAY2BGR).astype(np.uint8)

                    # writer.write(comm_diff)
                    frame_id += 1
            else:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
            
            frame0 = frame

        cap.release()
        # writer.release()

        out_csv_path = os.path.join(args.out, f"{os.path.basename(path)}.[{x},{y},{w},{h}].csv")
        df_marks = pd.DataFrame(motion_hist, columns=["motion"])
        df_marks.to_csv(out_csv_path)

        logging.info(f"Finished ... {out_csv_path}")

        



