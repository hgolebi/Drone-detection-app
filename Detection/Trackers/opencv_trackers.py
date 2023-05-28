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
        
        self.frame_check = 0
        self.last_trackers = np.array([])
    
    def update(self, bboxes, scores, frame):
        """ Update trackers and return new Track objects """
        self.frame_check += 1
        if self.frame_check == 1:
            self.update_trackers(bboxes, frame)
        elif self.frame_check == 3:
            self.frame_check = 0
        
        
        self.trackers.update(frame)
        # print(self.trackers.getObjects())
        self.remove_unused(frame)
        self.tracks = self.get_bboxes()

        

    def update_trackers(self, bboxes, frame):
        """Check IOU of newly detected bboxes """
        current_boxes = self.trackers.getObjects()
        for new_bbox in bboxes:
            if len(current_boxes) == 0 or not self.box_over_threshold(new_bbox, current_boxes):
                tracker = self.tracker_type()
                self.trackers.add(tracker, frame, new_bbox)
    
    # TODO remove
    # def box_over_threshold(self, bbox, bboxes, threshold = 0):
    #     """ Check if IOU is over set threshold """
    #     x, y, w, h = bbox
    #     bboxes = np.array(bboxes) # x1, y1, w1, h1
    #     x_left = np.maximum(bboxes[:, 0], x)
    #     y_top = np.maximum(bboxes[:, 1], y)
    #     x_right = np.minimum(x + w, bboxes[:, 0] + bboxes[:, 2])
    #     y_bottom = np.minimum(y + h, bboxes[:, 1] + bboxes[:, 3])
        
    #     intersection_area = (x_right - x_left) * (y_bottom - y_top)
        
    #     possible_idx = intersection_area>0
    #     intersection_area = intersection_area[possible_idx]

    #     union_area = w*h + bboxes[possible_idx, 2] * bboxes[possible_idx, 3] - intersection_area
    #     return np.any(intersection_area/union_area > threshold)
            
    def remove_unused(self, frame):
        trackers_arr = np.array(self.trackers.getObjects())
        arr1_shape = trackers_arr.shape[0]
        arr2_shape = self.last_trackers.shape[0]
        
        if arr1_shape > 0 and arr2_shape > 0 and arr1_shape == arr2_shape:
            comparison = np.all(np.isclose(trackers_arr, self.last_trackers, atol=.1), axis=1)
            idx = np.where(comparison, 1, 0)
            self.trackers = cv2.legacy.MultiTracker_create()
            print(idx, trackers_arr)
            for i, tracker_value in zip(idx, trackers_arr):
                if i == 0:
                    tracker = self.tracker_type()
                    self.trackers.add(tracker, frame, tuple(tracker_value))
        
        self.last_trackers = np.array(self.trackers.getObjects())

            
    
    def get_bboxes(self):
        """ Create Track objects """
        tracks = []
        bboxes = np.array(self.trackers.getObjects())
        if not bboxes.any():
            return []
        bboxes = self.xywh_to_xyxy(bboxes)
        for i, bbox in enumerate(bboxes):
            bbox = bbox.astype(int)
            tracks.append(Track(i, bbox))
        return tracks

