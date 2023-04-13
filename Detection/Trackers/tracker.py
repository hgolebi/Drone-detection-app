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

class Track:
    """ Track object stores track id and bounding box """
    def __init__(self, id, bbox):
        self.track_id = id
        self.bbox = bbox