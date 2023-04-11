import cv2
from tracker import Tracker, Track
import numpy as np
 
 
class OpenCVTracker(Tracker):
    names = {
        'KCF':cv2.TrackerKCF_create,
        'MEDIANFLOW':cv2.TrackerMedianFlow_create,
        'CSRT':cv2.TrackerCSRT_create}
    
    def __init__(self, name='CSRT'):
        self.trackers = cv2.MultiTracker_create()
        self.tracker_type = self.names[name]
    
    def update(self, bboxes, scores, frame):
        """
        1. create trackers for bboxes detected
        2. update trackers
        3. delete unused trackers
        4. create Tracks from bboxes
        """
        self.update_trackers(bboxes, frame)
        _, tracked_bboxes = self.trackers.update(frame)
        # self.delete_trackers(tracked_bboxes, bboxes)
        self.tracks = self.get_bboxes()

    # def delete_trackers(self, tracked_bboxes, bboxes):
    #     removed = []
    #     for i, b1, b2 in enumerate(zip(tracked_bboxes, bboxes)):
    #         if self.box_over_threshold(b1, b2, .95):
    #             removed.append(i)
        
        

    def update_trackers(self, bboxes, frame):
        for new_bbox in bboxes:
            found_bbox = False
            x = self.trackers.getObjects()
            for bbox in self.trackers.getObjects():
                bbox = bbox.astype(int)
                if self.box_over_threshold(new_bbox, bbox):
                    found_bbox = True
                    break
            if not found_bbox:
                tracker = self.tracker_type()
                self.trackers.add(tracker, frame, new_bbox)
    
    def box_over_threshold(self, bbox1, bbox2, threshold = .4):
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
        tracks = []
        bboxes = self.xywh_to_xyxy(np.array(self.trackers.getObjects()))
        for bbox in bboxes:
            bbox = bbox.astype(int)
            tracks.append(Track(999, bbox))
        return tracks
    
    def xywh_to_xyxy(self, bboxes):
        return np.hstack((bboxes[:, 0:2], bboxes[:, 0:2] + bboxes[:, 2:4] - 1))
    
    def xyxy_to_xywh(self, bboxes):
        return np.hstack((bboxes[:, 0:2], bboxes[:, 2:4] - bboxes[:, 0:2] + 1))