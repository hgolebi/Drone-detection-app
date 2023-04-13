import cv2
from tracker import Tracker, Track
import numpy as np
 
 
class OpenCVTracker(Tracker):
    """ Use cv.MultiTracker to implement 3 types of openCV trackers """
    names = {
        'KCF':cv2.legacy.TrackerKCF_create,
        'MEDIANFLOW':cv2.legacy.TrackerMedianFlow_create,
        'CSRT':cv2.legacy.TrackerCSRT_create}
    
    def __init__(self, name='CSRT'):
        self.trackers = cv2.legacy.MultiTracker_create()
        self.tracker_type = self.names[name]
    
    def update(self, bboxes, scores, frame):
        """ Update trackers and return new Track objects """
        self.update_trackers(bboxes, frame)
        self.trackers.update(frame)
        self.tracks = self.get_bboxes()

    def update_trackers(self, bboxes, frame):
        """Check IOU of newly detected bboxes """
        for new_bbox in bboxes:
            found_bbox = False
            for bbox in self.trackers.getObjects():
                bbox = bbox.astype(int)
                if self.box_over_threshold(new_bbox, bbox):
                    found_bbox = True
                    break
            if not found_bbox:
                tracker = self.tracker_type()
                self.trackers.add(tracker, frame, new_bbox)
    
    def box_over_threshold(self, bbox1, bbox2, threshold = .4):
        """ Check if IOU is over set threshold """
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)
        if x_right < x_left or y_bottom < y_top:
            return False
        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        union_area = w1 * h1 + w2 * h2 - intersection_area
        # print(intersection_area/union_area)
        return intersection_area/union_area > threshold
            
    
    def get_bboxes(self):
        """ Create Track objects """
        tracks = []
        bboxes = self.xywh_to_xyxy(np.array(self.trackers.getObjects()))
        for bbox in bboxes:
            bbox = bbox.astype(int)
            # TODO id
            tracks.append(Track(999, bbox))
        return tracks
