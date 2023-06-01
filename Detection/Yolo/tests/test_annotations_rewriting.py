import unittest
import cv2
import os
from unittest.mock import MagicMock
from annotations_rewriting import AnnotationsRewriter

class AnnotationsRewriterTests(unittest.TestCase):

    def setUp(self):
        self.rewriter = AnnotationsRewriter()

    def tearDown(self):
        pass

    def test_load_dimensions_from_file(self):
        with open("temp_dimensions.txt", 'w') as file:
            file.write("1920.0, 1080.0\n")
            file.write("1280.0, 720.0\n")

        self.rewriter.load_dimensions_from_file("temp_dimensions.txt")

        self.assertEqual(self.rewriter.dimensions, [(1920.0, 1080.0), (1280.0, 720.0)])

        os.remove("temp_dimensions.txt")

    def test_calculate_dimensions(self):
        mock_video_capture = MagicMock(spec=cv2.VideoCapture)
        mock_video_capture.isOpened.return_value = True
        mock_video_capture.get.side_effect = 1920.0, 1080.0, 1920.0, 1080.0

        cv2.VideoCapture = MagicMock(return_value=mock_video_capture)

        os.makedirs("temp_videos")
        open("temp_videos/video1.mp4", "w").close()
        open("temp_videos/video2.mp4", "w").close()

        temp_val = self.rewriter.dimensions
        self.rewriter.calculate_dimensions("temp_videos")
        print(self.rewriter.dimensions)

        self.assertEqual(self.rewriter.dimensions, [(1920.0, 1080.0), (1920.0, 1080.0)])

        os.remove("temp_videos/video1.mp4")
        os.remove("temp_videos/video2.mp4")
        os.rmdir("temp_videos")

    def test_save_dimensions_to_file(self):
        self.rewriter.dimensions = [(1920.0, 1080.0), (1280.0, 720.0)]

        self.rewriter.save_dimensions_to_file("temp_dimensions.txt")

        with open("temp_dimensions.txt", 'r') as file:
            lines = file.readlines()

        self.assertEqual(lines, ["1920.0, 1080.0\n", "1280.0, 720.0"])

        os.remove("temp_dimensions.txt")

    def test_change_to_yolo_format(self):
        line = "25 1 123 456 789 899 drone"
        width = 1920
        height = 1080

        new_anns = self.rewriter.change_to_yolo_format(line, width, height)

        self.assertEqual(new_anns, ["0 0.26953125 0.8384259259259259 0.4109375 0.8324074074074074"])

    def test_convert_drone_coordinates(self):
        drone = ["123", "456", "789", "1111"]
        width = 1920
        height = 1080

        new_drone = self.rewriter.convert_drone_coordinates(drone, width, height)

        self.assertEqual(new_drone, ['0.26953125', '0.9365740740740741', '0.4109375', '1.0287037037037037'])

    def test_write_each_ann_to_single_file(self):
        os.makedirs("temp_annotations")
        open("temp_annotations/annotation1.txt", "w").write("1 0 123 456 789 600\n")
        open("temp_annotations/annotation2.txt", "w").write("2 1 234 567 890 748\n")

        dimensions = [(1920, 1080), (1280, 720)]

        os.makedirs("temp_output")

        self.rewriter.write_each_ann_to_single_file("temp_annotations", dimensions, "temp_output")

        self.assertTrue(os.path.exists("temp_output/annotation1_frame_00001.txt"))
        self.assertTrue(os.path.exists("temp_output/annotation2_frame_00002.txt"))

        os.remove("temp_annotations/annotation1.txt")
        os.remove("temp_annotations/annotation2.txt")
        os.rmdir("temp_annotations")
        os.remove("temp_output/annotation1_frame_00001.txt")
        os.remove("temp_output/annotation2_frame_00002.txt")
        os.rmdir("temp_output")

if __name__ == '__main__':
    unittest.main()
