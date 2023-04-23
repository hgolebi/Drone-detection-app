from deep_sort.deep_sort.tracker import Tracker as DeepSort
from deep_sort.tools import generate_detections as gdet
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection

from sort.sort import Sort
from tracker import Tracker, Track
import numpy as np
from pathlib import Path

from Trackers import encoder_dir

class DeepSortTracker(Tracker):
    """ Utilize DeepSort library with it's box encoder to track objects. """
    def __init__(self, metric=None, encoder_filename=f'{encoder_dir}\mars-small128.pb'):
        if metric is None:
            metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.4)
        self.deep_sort = DeepSort(metric)
        
        
        self.encoder = gdet.create_box_encoder(encoder_filename, batch_size=16)
        

    def update(self, bboxes, scores, frame):
        """ Update tracker using bboxes with standard xywh format (not YOLO xywh format!)"""
        features = self.encoder(frame, bboxes)

        detections_scores_features = []
        for bbox_id, bbox in enumerate(bboxes):
            detections_scores_features.append(Detection(bbox, scores[bbox_id], features[bbox_id]))

        self.deep_sort.predict()
        self.deep_sort.update(detections_scores_features)
        self.update_tracks()
        return self.tracks

    def update_tracks(self):
        """ Create Track objects from confirmed tracks  """
        tracks = []
        for track in self.deep_sort.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            id = track.track_id

            tracks.append(Track(id, bbox))

        self.tracks = tracks

class SortTracker(Tracker):
    """ Utilize Sort library to track objects """
    def __init__(self):
        self.sort = Sort(max_age=1, min_hits=3, iou_threshold=0.6)
        self.tracks = []
    
    def update(self, bboxes, scores, frame=None):
        """ Convert bboxes and scores to right format and upadte tracks """
        bboxes = self.xywh_to_xyxy(np.array(bboxes).reshape(-1, 4))
        scores = np.array(scores).reshape(-1, 1)
        detections = np.c_[bboxes, scores]
        
        tracked = self.sort.update(detections)
        
        self.tracks.clear()
        for *bbox, box_id in tracked:
            box_id = int(box_id)
            self.tracks.append(Track(box_id, bbox))
        return self.tracks
