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
        current_boxes = self.trackers.getObjects()
        for new_bbox in bboxes:
            if len(current_boxes) == 0 or not self.box_over_threshold(new_bbox, current_boxes):
                tracker = self.tracker_type()
                self.trackers.add(tracker, frame, new_bbox)
    
    def box_over_threshold(self, bbox, bboxes, threshold = .4):
        """ Check if IOU is over set threshold """
        x, y, w, h = bbox
        bboxes = np.array(bboxes) # x1, y1, w1, h1
        x_left = np.maximum(bboxes[:, 0], x)
        y_top = np.maximum(bboxes[:, 1], y)
        x_right = np.minimum(x + w, bboxes[:, 0] + bboxes[:, 2])
        y_bottom = np.minimum(y + h, bboxes[:, 1] + bboxes[:, 3])
        
        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        
        possible_idx = intersection_area>0
        intersection_area = intersection_area[possible_idx]

        union_area = w*h + bboxes[possible_idx, 2] * bboxes[possible_idx, 3] - intersection_area
        return np.any(intersection_area/union_area > threshold)
            
    # def remove_unused(self):
    #     arr = np.array(self.trackers.getObjects())
    #     mask = (arr >= 0).all(axis=1)
    #     idx = np.where(mask)[0]
        
    #     trackers = []
            
    
    def get_bboxes(self):
        """ Create Track objects """
        tracks = []
        bboxes = self.xywh_to_xyxy(np.array(self.trackers.getObjects()))
        for i, bbox in enumerate(bboxes):
            bbox = bbox.astype(int)
            tracks.append(Track(i, bbox))
        return tracks

