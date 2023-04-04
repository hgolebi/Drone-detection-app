from deep_sort.deep_sort.tracker import Tracker as DeepSort
from deep_sort.tools import generate_detections as gdet
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection

from sort.sort import Sort
from tracker import Tracker, Track
import numpy as np

class DeepSortTracker(Tracker):
    def __init__(self, metric=None, encoder_filename='./mars-small128.pb'):
        if metric is None:
            metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.4)
        self.deep_sort = DeepSort(metric)
        
        self.encoder = gdet.create_box_encoder(encoder_filename, batch_size=16)
        

    def update(self, bboxes, scores, frame):
        """updates tracker using bboxes with xywh format (where x is left x, not yolo format)
        """
        features = self.encoder(frame, bboxes)

        detections_scores_features = []
        for bbox_id, bbox in enumerate(bboxes):
            detections_scores_features.append(Detection(bbox, scores[bbox_id], features[bbox_id]))

        self.deep_sort.predict()
        self.deep_sort.update(detections_scores_features)
        self.update_tracks()
        return self.tracks

    def update_tracks(self):
        tracks = []
        for track in self.deep_sort.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            id = track.track_id

            tracks.append(Track(id, bbox))

        self.tracks = tracks

class SortTracker(Tracker):
    def __init__(self):
        self.sort = Sort(max_age=1, min_hits=3, iou_threshold=0.6)
        self.tracks = []
    
    def update(self, bboxes, scores, frame=None):
        bboxes = np.array(bboxes)
        scores = np.array(scores).reshape(-1, 1)
        detections = np.c_[bboxes, scores]
        track_bbs_ids = self.sort.update(detections)
        
        for bbox, box_id in zip(bboxes, track_bbs_ids):
            box_id = int(box_id[0])
            self.tracks.append(Track(box_id, bbox))
        return self.tracks

