import numpy as np
import cv2 as cv
from random import random
from tracker import Tracker, Track

class OpticalFlow(Tracker):
    def __init__(self):
        self.last_frame = None
        self.curr_frame = None
        self.tracks = []
        self.id = 0
        self.last_trackers = np.array([])
    
    def get_id(self):
        self.id += 1 
        return self.id

    def update(self, bboxes, scores, frame):
        if self.last_frame is not None:
            self.curr_frame = self.convert_frame_to_gray(frame.copy())
            # TODO refactor flow call
            flow = self.calculate_flow(self.last_frame, self.curr_frame)
            new_bboxes = self.get_bbox_from_flow(flow)
            # print(new_bboxes)
            self.compare_boxes(new_bboxes, bboxes)
            print(self.tracks)
            self.last_frame = self.curr_frame.copy()
        else:
            self.last_frame = self.convert_frame_to_gray(frame)
    
    def get_bbox_from_flow(self, flow_map):
        """ return xywh bbox from flow """
        magnitude, _ = cv.cartToPolar(flow_map[..., 0], flow_map[..., 1])
        filtered_magnitude = magnitude > 2
        contours, _ = cv.findContours(filtered_magnitude.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        bounding_boxes = np.array([cv.boundingRect(contour) for contour in contours])
        if bounding_boxes.ndim == 2:
            bounding_boxes = bounding_boxes[np.all(bounding_boxes>6, axis=1)]

        return np.array(bounding_boxes)
    
    def compare_boxes(self, bounding_boxes, yolo_bboxes=None):
        """ bounding_boxes xywh, yolo_bboxes xywh, Track in xyxy """
        if self.tracks == [] and yolo_bboxes is not None and yolo_bboxes != []:
            self.tracks = [Track(self.get_id(), box) for box in self.xywh_to_xyxy(np.array(yolo_bboxes))]
        elif self.tracks != [] and bounding_boxes.ndim == 2:
            new_tracks = []
            curr_bboxes = [track.get_xywh() for track in self.tracks]
            ids_found = set()
            
            for bbox, track_bbox in zip(bounding_boxes, self.xywh_to_xyxy(bounding_boxes)):
                bbox_found = self.box_over_threshold(bbox, curr_bboxes, threshold=.4, get_idx=True)
                
                if bbox_found is not None and self.tracks[bbox_found].track_id not in ids_found:
                    new_tracks.append(Track(self.tracks[bbox_found].track_id, track_bbox))
                    ids_found.add(self.tracks[bbox_found].track_id)
                elif yolo_bboxes is not None and len(yolo_bboxes) != 0 and self.box_over_threshold(bbox, yolo_bboxes, threshold=0.7):
                    new_tracks.append(Track(self.get_id(), track_bbox))
            
            for track in self.tracks:
                if track.track_id not in ids_found:
                    track.last_updated += 1
                    if track.last_updated < 5:
                        new_tracks.append(track)
            
            self.tracks = sorted(new_tracks, key=lambda t: t.track_id)
    
    def convert_frame_to_gray(self, frame):
        """converts frame from RGB to GRAY color"""
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    def calculate_flow(self, frame_prev, frame_next):
        """calculates optical flow based on two RGB frames"""

        return cv.calcOpticalFlowFarneback(frame_prev, frame_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    
    
    

if __name__ == '__main__':
    of = OpticalFlow()
    video_in = cv.VideoCapture("./walk.mp4")
    print(video_in.get(cv.CAP_PROP_FPS))
    ret, prev_frame = video_in.read()
    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(10)]
    for i in range(30):
        ret, current_frame = video_in.read()
        f1 = of.convert_frame_to_gray(prev_frame.copy())
        f2 = of.convert_frame_to_gray(current_frame.copy())
        flow = of.calculate_flow(f1, f2)
        prev_frame = current_frame.copy()
        
        for track in of.get_bbox_from_flow(flow):
            x1, y1, x2, y2 = track
            print(x1, y1, x2, y2)
            cv.rectangle(current_frame, (int(x1), int(y1)), (int(x1 + x2), int(y1 + y2)), (colors[12 % len(colors)]), 3)

        cv.imshow("current_frame", current_frame)
        k = cv.waitKey(30) & 0xff
    