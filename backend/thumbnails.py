import os
import subprocess
import cv2
import tempfile
import numpy as np


def thumbnail_name(videoname: str):
    return "-".join(videoname.split('.'))+".png"


def generate_thumbnail(filename, n=30):

    cap = cv2.VideoCapture(f"./backend/tmp/{filename}")
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
    print(video_length)
    # image = np.zeros((720,1280,3), dtype=np.uint8)
    if cap.isOpened() and video_length > 0:
        succes, image = cap.read()
        i = 0
        new_image = image
        while succes and i < n:
            image = new_image
            succes, new_image = cap.read()
            i += 1
        cv2.imwrite(f"./backend/tmp/{thumbnail_name(filename)}", image)
        return
    cv2.imwrite(f"./backend/tmp/{thumbnail_name(filename)}",
                np.zeros((720, 1280, 3), dtype=np.uint8))


def check_thumbnail(self, videname: str):
    thumb_name = self.thumbnail_name(videname)
