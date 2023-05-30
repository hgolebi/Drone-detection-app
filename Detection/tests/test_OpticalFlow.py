import unittest
import numpy as np
from Trackers.tracker import Track
from Trackers.optical_flow import OpticalFlow

class OpticalFlowTestCase(unittest.TestCase):
    
    def setUp(self):
        self.optical_flow = OpticalFlow()

    def test_get_id(self):
        self.assertEqual(self.optical_flow.get_id(), 1)

    def test_convert_frame_to_gray(self):
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        gray_frame = self.optical_flow.convert_frame_to_gray(frame)
        self.assertEqual(gray_frame.shape, (100, 100))

    def test_calculate_flow(self):
        frame_prev = self.optical_flow.convert_frame_to_gray(np.zeros((100, 100, 3), dtype=np.uint8))
        frame_next = self.optical_flow.convert_frame_to_gray(np.zeros((100, 100, 3), dtype=np.uint8))
        flow = self.optical_flow.calculate_flow(frame_prev, frame_next)
        self.assertEqual(flow.shape, (100, 100, 2))

    def test_get_bbox_from_flow(self):
        flow_map = np.zeros((100, 100, 2), dtype=np.float32)
        bounding_boxes = np.array(self.optical_flow.get_bbox_from_flow(flow_map))
        self.assertEqual(len(bounding_boxes), 0)

    def test_compare_boxes_no_existing_tracks(self):
        bounding_boxes = np.array(np.array([(10, 10, 20, 20), (30, 30, 40, 40)]))
        self.optical_flow.compare_boxes(bounding_boxes, bounding_boxes)
        self.assertEqual(len(self.optical_flow.tracks), 2)

    def test_compare_boxes_with_existing_tracks(self):
        self.optical_flow.tracks = [Track(1, (10, 10, 20, 20))]
        bounding_boxes = np.array(np.array([(10, 10, 20, 20), (30, 30, 40, 40)]))
        self.optical_flow.compare_boxes(bounding_boxes, bounding_boxes)
        # self.assertEqual(len(self.optical_flow.tracks), 2)
    
    def test_track_changes(self):
        bounding_boxes = np.array([(10, 10, 20, 20), (30, 30, 40, 40)])
        self.optical_flow.compare_boxes(bounding_boxes, bounding_boxes)
        self.assertEqual(len(self.optical_flow.tracks), 2) 
        self.assertEqual(self.optical_flow.tracks[0].track_id, 1)
        self.assertEqual(self.optical_flow.tracks[1].track_id, 2)
        
        bounding_boxes2 = np.array([(10, 10, 20, 20), (31, 31, 40, 40), (31, 31, 39, 39), (31, 31, 40, 40)])
        self.optical_flow.compare_boxes(bounding_boxes2)
        self.assertEqual(self.optical_flow.tracks[0].track_id, 1)
        self.assertTrue(all(self.optical_flow.tracks[0].bbox == (10, 10, 20, 20)))
        
        self.assertEqual(self.optical_flow.tracks[1].track_id, 2)
        self.assertTrue(all(self.optical_flow.tracks[1].bbox == (31, 31, 40, 40)))

if __name__ == '__main__':
    unittest.main()
