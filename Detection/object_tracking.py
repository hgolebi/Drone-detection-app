from Trackers.opencv_trackers import OpenCVTracker
from Trackers.deep_sort_tracker import DeepSortTracker, SortTracker
from ultralytics import YOLO
import torch
import cv2
import random
from Detection.Yolo import model_dir
import sys

class ObjectTracking:
    def __init__(self, yolo_path=f'{model_dir}/best.pt', tracker=DeepSortTracker()):
        self.yolo = YOLO(yolo_path)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.yolo.to(device)
        
        self.tracker = tracker
        # TODO tracker choose option or sth
        
    def get_video(self, video_path_in, video_path_out='out.mp4'):
        self.video_in = cv2.VideoCapture(video_path_in)
        self.next_frame()
        
        self.cap_out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), self.video_in.get(cv2.CAP_PROP_FPS), (self.frame.shape[1], self.frame.shape[0]))
        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(10)]
    
    def write_video(self):
        for track in ot.tracker.tracks:
            x1, y1, x2, y2 = track.bbox
            cv2.rectangle(self.frame, (int(x1), int(y1)), (int(x2), int(y2)), (self.colors[track.track_id % len(self.colors)]), 3)
        
        self.cap_out.write(self.frame)

    
    def detect(self, threshold=.5):
        current_frame = self.frame
        [results] = self.yolo(current_frame)
        
        boxes = []
        scores = []
        for box, score, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
            score = score.item()
            box = [int(item) for item in box]
            if score > threshold:
                boxes.append(self.yolo_box_to_box(box))
                scores.append(score)
        
        # TODO filter classes ?
        
        self.next_frame()
        return boxes, scores, current_frame
    
    def yolo_box_to_box(self, box):
        # TODO refactor maybe
        return box[0], box[1], box[2] - box[0], box[3] - box[1]
    
    def update_tracker(self, boxes, scores, frame):
        # TODO
        self.tracker.update(boxes, scores, frame)

    def run(self, frame_dillation=None):
        # detect every x frames, update tracker, return video
        while ot.frame_returned:
            detect_tuple = ot.detect()
            ot.update_tracker(*detect_tuple)
            ot.write_video()
    
    def next_frame(self):
        self.frame_returned, self.frame = self.video_in.read()
    
if __name__ == "__main__":
    ot = ObjectTracking()
    if len(sys.argv) > 1:
        ot.get_video(sys.argv[1])
    else:
        ot.get_video('Detection/Trackers/walk.mp4')
    
    ot.run()
