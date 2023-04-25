import numpy as np
import torch
import cv2 as cv
from ultralytics import YOLO
from Optical_Flow.optical_flow import OpticalFlow

class ObjectDetector:
    def __init__(self, weights_path):
        self.weights = weights_path
        self.model = YOLO(weights_path)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(device)

    def detect_objects(self, frame):
        """detects objects using YOLO model"""
        detections = self.model.predict(frame)
        return detections

    def draw_boxes(self, frame, boxes):
        """draws bounding boxes on the frame"""
        for box in boxes:
            x, y, w, h = map(int, box[:4])
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    def get_new_box_with_optical_flow(self, box, flow, prev_boxes=False):
        """calculates new box position using optical flow"""
        cx, cy, w, h = map(int, box[:4])
        new_cx = int(cx + flow[cy:cy+h, cx:cx+w, 0].mean())
        new_cy = int(cy + flow[cy:cy+h, cx:cx+w, 1].mean())
        new_x = int(new_cx - w / 2)
        new_y = int(new_cy - h / 2)
        new_box = [new_x, new_y, w, h]
        return new_box

    def run(self, video_file):
        cap = cv.VideoCapture(cv.samples.findFile(video_file))

        of = OpticalFlow()

        ret, frame1 = cap.read()
        results1 = self.detect_objects(frame1)
        prev_boxes = results1[0].boxes

        while ret: 
            ret, frame2 = cap.read()
            results2 = self.detect_objects(frame2)

            flow = of.calculate_flow(frame1, frame2)

            boxes1 = results1[0].boxes
            new_boxes1 = []
            # if zero drones detected -> instead of using detection's boxes 
            # use boxes calculated for previous frame
            if len(results1[0].boxes) == 0:
                for box in prev_boxes:
                    new_boxes1.append(self.get_new_box_with_optical_flow(box, flow))
            else:
                for box in boxes1:
                    box = box.xywh.squeeze()
                    new_boxes1.append(self.get_new_box_with_optical_flow(box, flow))

            self.draw_boxes(frame2, new_boxes1)

            cv.imshow('frame2', frame2)
            k = cv.waitKey(30) & 0xff

            prev_boxes = new_boxes1
            frame1 = frame2
            results1 = results2

if __name__ == '__main__':
    ob_det = ObjectDetector('Yolo/models/best.pt')
    ob_det.run("Yolo/GOPR5842_005.mp4")