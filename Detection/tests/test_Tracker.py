import unittest
import numpy as np
from Trackers.tracker import Tracker, Track

class TestTracker(Tracker):
    def update(self, bboxes, scores, frame):
        pass


class TestTrackerMethods(unittest.TestCase):

    def setUp(self):
        self.tracker = TestTracker()

    def test_xywh_to_xyxy(self):
        xywh = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        expected = np.array([[1, 2, 3, 5], [5, 6, 11, 13]])
        result = self.tracker.xywh_to_xyxy(xywh)
        np.testing.assert_array_equal(result, expected)

    def test_xyxy_to_xywh(self):
        xyxy = np.array([[1, 2, 3, 5], [5, 6, 11, 13]])
        expected = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        result = self.tracker.xyxy_to_xywh(xyxy)
        np.testing.assert_array_equal(result, expected)

    def test_box_over_threshold(self):
        bbox = [0, 0, 10, 10]
        bboxes = [[12, 12, 10, 10], [0, 0, 8, 8], [1, 1, 4, 3]]
        threshold = 0.3

        result1 = self.tracker.box_over_threshold(bbox, bboxes, threshold)
        self.assertTrue(result1)

        result2 = self.tracker.box_over_threshold(bbox, bboxes, threshold, get_idx=True)
        self.assertEqual(result2, 1)
    
    def test_no_box_over_threshold(self):
        bbox = [0, 0, 10, 10]
        bboxes = [[12, 12, 10, 10], [1, 1, 4, 3]]
        threshold = 0.3

        result1 = self.tracker.box_over_threshold(bbox, bboxes, threshold)
        self.assertFalse(result1)

        result2 = self.tracker.box_over_threshold(bbox, bboxes, threshold, get_idx=True)
        self.assertEqual(result2, None)
        


class TestTrack(unittest.TestCase):

    def test_track_init(self):
        track_id = 1
        bbox = [1, 2, 3, 4]
        track = Track(track_id, bbox)
        self.assertEqual(track.track_id, track_id)
        np.testing.assert_array_equal(track.bbox, bbox)

if __name__ == '__main__':
    unittest.main()
