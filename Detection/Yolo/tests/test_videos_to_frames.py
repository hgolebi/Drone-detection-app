import unittest
import cv2
import os
import numpy as np
from unittest.mock import MagicMock
from videos_to_frames import VideoProcessor

class TestVideoProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = VideoProcessor()

    def tearDown(self):
        pass

    def test_count_lines_in_files(self):
        os.makedirs("temp_annotations")
        with open("temp_annotations/annotations1.txt", "w") as file1:
            file1.write("Line 1\nLine 2\nLine 3")
        with open("temp_annotations/annotations2.txt", "w") as file2:
            file2.write("Line 1\nLine 2")

        result = self.processor.count_lines_in_files("temp_annotations")

        self.assertEqual(result, [3, 2])

        os.remove("temp_annotations/annotations1.txt")
        os.remove("temp_annotations/annotations2.txt")
        os.rmdir("temp_annotations")

    def test_save_video_frames_as_jpg(self):
        mock_video_capture = MagicMock()
        mock_video_capture.isOpened.return_value = True
        mock_video_capture.get.return_value = 100
        mock_video_capture.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)

        cv2.VideoCapture = MagicMock(return_value=mock_video_capture)

        os.makedirs("temp_videos")
        open("temp_videos/video1.mp4", "w").close()
        open("temp_videos/video2.mp4", "w").close()

        self.processor.save_video_frames_as_jpg("temp_videos", [1, 1], "output_frames")

        self.assertTrue(os.path.exists("output_frames/video1_frame_00000.jpg"))
        self.assertTrue(os.path.exists("output_frames/video2_frame_00000.jpg"))

        os.remove("temp_videos/video1.mp4")
        os.remove("temp_videos/video2.mp4")
        os.rmdir("temp_videos")
        for file in os.listdir("output_frames"):
            os.remove(os.path.join("output_frames", file))
        os.rmdir("output_frames")


    def test_extract_frame(self):
        mock_video_capture = MagicMock()
        mock_video_capture.set.return_value = None
        mock_video_capture.read.return_value = True, "Test frame"

        frame = self.processor.extract_frame(mock_video_capture, 10)

        self.assertEqual(frame, "Test frame")

if __name__ == '__main__':
    unittest.main()
