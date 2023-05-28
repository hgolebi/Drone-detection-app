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
        return np.hstack((bboxes[:, 0:2], bboxes[:, 0:2] + bboxes[:, 2:4] - 1))
    
    def xyxy_to_xywh(self, bboxes):
        """ convert bboxes from xyxy to xywh format """
        return np.hstack((bboxes[:, 0:2], bboxes[:, 2:4] - bboxes[:, 0:2] + 1))
    
    def box_over_threshold(self, bbox, bboxes, threshold = 0, get_idx=False):
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
        
        iou = intersection_area / union_area
        
        
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
    """ Track object stores track id and bounding box """
    def __init__(self, id, bbox):
        self.track_id = id
        self.bbox = bbox
    
    def __repr__(self):
        return f"<Track ID: {self.track_id}, Bounding Box: {self.bbox}>"