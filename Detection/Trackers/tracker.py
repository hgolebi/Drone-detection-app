from abc import ABC, abstractmethod

class Tracker(ABC):    
    @abstractmethod
    def update(self, bboxes, scores, frame):
        pass

class Track:
    def __init__(self, id, bbox):
        self.track_id = id
        self.bbox = bbox