import unittest
import cv2
from datetime import datetime
from pathlib import Path

from Trackers.deep_sort_tracker import DeepSortTracker, SortTracker
from Trackers.opencv_trackers import OpenCVTracker
from Detection.object_tracking import ObjectTracking
from tests import test_files_dir

from Trackers.deep_sort.deep_sort import nn_matching

import logging
logging.getLogger().setLevel(logging.WARNING)

from Trackers.deep_sort.deep_sort.tracker import Tracker as DeepSort

class VideoProcessingTestCase(unittest.TestCase):
    
    def test_ids(self):
        names = ['sort', 'deepsort', 'kcf', 'medianflow', 'csrt']
        results = []
        for name in names:
            res = f'{name}: {self.last_line(name)}'
            results.append(res)
        for line in results:
            print(line)

    def last_line(self, name):
        video_path = f'{test_files_dir}\drone_presentation.mp4'
        out_name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + '.mp4'
        ot = ObjectTracking('name')
        ot.get_video(video_path)
        ot.run()
        print(ot.object_counter)
        return ot.object_counter

    # Add more test methods as needed