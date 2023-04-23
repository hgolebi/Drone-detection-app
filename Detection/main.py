from Trackers.opencv_trackers import OpenCVTracker
from Trackers.deep_sort_tracker import DeepSortTracker, SortTracker
from ultralytics import YOLO
import torch
import cv2

class ObjectTracking:
    def __init__(self, yolo_path='./models/best.pt', tracker=DeepSortTracker()):
        self.yolo = YOLO(yolo_path)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.yolo.to(device)
        
        self.tracker = tracker
        # TODO tracker choose option or sth
        
    def get_video(self, video_path_in, video_path_out='out.mp4'):
        self.video_in = cv2.VideoCapture(video_path_in)
        ret, frame = self.video_in.read()
        # TODO do get frame shape without this
        
        self.cap_out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), self.video_in.get(cv2.CAP_PROP_FPS), (frame.shape[1], frame.shape[0]))

    
    def detect(self, frame, threshold=.5):
        [results] = self.yolo(frame)
        
        boxes = []
        scores = []
        for box, score, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
            score = score.item()
            box = [int(item) for item in box]
            if score > threshold:
                boxes.append(self.yolo_box_to_box(box))
                scores.append(score)
        
        # TODO filter classes ?

        return boxes, scores, frame
    
    def yolo_box_to_box(self, box):
        # TODO refactor maybe
        return box[0], box[1], box[2] - box[0], box[3] - box[1]
    
    def update_tracker(self, boxes, scores, frame):
        # TODO
        self.tracker.update(boxes, scores, frame)

    def run(self, frame_dillation):
        # detect every x frames, update tracker, return video
        pass