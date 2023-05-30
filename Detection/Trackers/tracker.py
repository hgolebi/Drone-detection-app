from abc import ABC, abstractmethod
import numpy as np

class Tracker(ABC):
    """ Abstract Tracker class implements update method and 2 concrete methods of bbox conversion """

    @abstractmethod
    def update(self, bboxes, scores, frame):
        """ Return updated Track list
        Args:
            bboxes : bboxes in xywh format
            scores : 2d list of scores
            frame : image frame
        """
        pass
    
    def xywh_to_xyxy(self, bboxes):
        """ convert bboxes from xywh to xyxy format """
        return np.hstack((bboxes[:, 0:2], bboxes[:, 0:2] + bboxes[:, 2:4]))
    
    def xyxy_to_xywh(self, bboxes):
        """ convert bboxes from xyxy to xywh format """
        return np.hstack((bboxes[:, 0:2], bboxes[:, 2:4] - bboxes[:, 0:2]))
    
    def box_over_threshold(self, bbox, bboxes, threshold = 0, get_idx=False):
        """ Check if IOU is over set threshold """
        # print(bbox)
        # print(bboxes)
        x, y, w, h = bbox
        bboxes = np.array(bboxes) # x1, y1, w1, h1
        x_left = np.maximum(bboxes[:, 0], x)
        y_top = np.maximum(bboxes[:, 1], y)
        x_right = np.minimum(x + w, bboxes[:, 0] + bboxes[:, 2])
        y_bottom = np.minimum(y + h, bboxes[:, 1] + bboxes[:, 3])
        
        intersection_area = np.maximum(0, x_right - x_left) * np.maximum(0, y_bottom - y_top)
        
        possible_idx = intersection_area>0
        intersection_area = intersection_area[possible_idx]

        union_area = w*h + bboxes[possible_idx, 2] * bboxes[possible_idx, 3] - intersection_area
        
        iou = intersection_area / union_area
        
        if np.any(iou > 1) :
            raise ValueError(1)
        # print(iou)
        if get_idx:
            indices = np.where(possible_idx)[0]
            idx_found = np.where(iou > threshold)[0]
            if idx_found.size:
                return indices[idx_found].min()
            else:
                return None
        else:
            return np.any(iou > threshold)
        

class Track:
    """ Track object stores track id and bounding box as xyxy """
    def __init__(self, id, bbox, last_updated=0):
        self.track_id = id
        self.bbox = bbox
        self.last_updated = last_updated
    
    def __repr__(self):
        return f"<Track ID: {self.track_id}, Bounding Box: {self.bbox}>"
    
    def get_xywh(self):
        return (self.bbox[0], self.bbox[1], self.bbox[2] - self.bbox[0], self.bbox[3] - self.bbox[1])