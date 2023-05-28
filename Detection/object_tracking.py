from Trackers.opencv_trackers import OpenCVTracker
from Trackers.optical_flow import OpticalFlow
from Trackers.deep_sort_tracker import DeepSortTracker, SortTracker
from ultralytics import YOLO
import torch
import cv2
import random
from Detection.Yolo import model_dir
import sys
from io import StringIO


class ObjectTracking:
    def __init__(self, name='', yolo_path=f'{model_dir}/best.pt'):
        self.yolo = YOLO(yolo_path)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.yolo.to(device)

        self.tracker = self.get_tracker(name)
        self.adnotations = []
        self.frame_counter = 0
        self.object_counter = 0
        
    def get_tracker(self, name):
        tracker_dict = {
            'deepsort': DeepSortTracker(), 'sort': SortTracker(),
            'kcf': OpenCVTracker('KCF'), 'medianflow': OpenCVTracker('MEDIANFLOW'), 'csrt': OpenCVTracker(),
            'optical_flow': OpticalFlow()
        }
        return tracker_dict.get(name.lower(), OpenCVTracker())

    def get_video(self, video_path_in, video_path_out='out.mp4'):
        self.video_in = cv2.VideoCapture(video_path_in)
        self.next_frame()

        # TODO return fps
        self.cap_out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(
            *'mp4v'), self.video_in.get(cv2.CAP_PROP_FPS), (self.frame.shape[1], self.frame.shape[0]))
        self.colors = [(random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255)) for _ in range(10)]

    def write_video(self):
        for track in self.tracker.tracks:
            x1, y1, x2, y2 = track.bbox
            self.adnotations.append([self.frame_counter, track.track_id, x1, y1, x2, y2])
            cv2.rectangle(self.frame, (int(x1), int(y1)), (int(x2), int(y2)), (self.colors[track.track_id % len(self.colors)]), 3)
            self.object_counter = track.track_id
        
        self.cap_out.write(self.frame)

    def detect(self, threshold=.3):
        if isinstance(self.tracker, OpticalFlow):
            self.next_frame()
            return None, None, self.frame
        
        #TODO threshold to self.
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


        self.next_frame()
        return boxes, scores, current_frame

    def yolo_box_to_box(self, box):
        return box[0], box[1], box[2] - box[0], box[3] - box[1]

    def update_tracker(self, boxes, scores, frame):
        # TODO
        self.tracker.update(boxes, scores, frame)

    def run(self, frame_dillation=None):
        # detect every x frames, update tracker, return video
        while self.frame_returned:
            detect_tuple = self.detect()
            self.update_tracker(*detect_tuple)
            self.write_video()
        
        self.save_adnotations()
        self.video_in.release()
    
    def next_frame(self):
        self.frame_returned, self.frame = self.video_in.read()
        self.frame_counter += 1
    
    def save_adnotations(self):
        self.text_file = StringIO()
        for item in self.adnotations:
            self.text_file.write(', '.join(str(num) for num in item) + '\n')
        self.text_file.seek(0)
    
if __name__ == "__main__":
    ot = ObjectTracking(name='optical_flow')
    if len(sys.argv) > 1:
        ot.get_video(sys.argv[1])
    else:
        ot.get_video('Detection/Trackers/walk.mp4')
    
    ot.run()