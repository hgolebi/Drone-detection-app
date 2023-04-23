import numpy as np
import cv2 as cv
from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, weights_path):
        self.model = YOLO(weights_path)

    def detect_objects(self, frame):
        """detects objects using YOLO model"""
        detections = self.model.predict(frame)
        return detections

    def draw_boxes(self, frame, boxes):
        """draws bounding boxes on the frame"""
        for box in boxes:
            x, y, w, h = map(int, box[:4])
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

class OpticalFlow:
    def convert_frame_to_gray(self, frame):
        """converts frame from RGB to GRAY color"""
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    def calculate_flow(self, frame_prev, frame_next):
        """calculates optical flow based on two RGB frames"""
        frame_prev = self.convert_frame_to_gray(frame_prev)
        frame_next = self.convert_frame_to_gray(frame_next)
        return cv.calcOpticalFlowFarneback(frame_prev, frame_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    def map_flow(self, flow):
        """maps flow on rgb frame with shape as input frames"""
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv = np.zeros(shape=(*ang.shape, 3), dtype=np.uint8)
        hsv[..., 0] = ang*180/np.pi/2
        hsv[..., 1] = 255
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        return bgr

if __name__ == '__main__':
    cap = cv.VideoCapture(cv.samples.findFile("./walk.mp4"))

    of = OpticalFlow()
    obj_detector = ObjectDetector('yolov8s.pt')

    ret, frame1 = cap.read()
    results1 = obj_detector.detect_objects(frame1)
    
    while True:
        ret, frame2 = cap.read()
        results2 = obj_detector.detect_objects(frame2)

        flow = of.calculate_flow(frame1, frame2)
        new_boxes1 = []
        for r in results1:
            boxes1 = r.boxes
            for i, box in enumerate(boxes1):
                # calculate new box position using optical flow
                box = box.xywh.squeeze()
                cx, cy, w, h = map(int, box[:4])
                new_cx = int(cx + flow[cy:cy+h, cx:cx+w, 0].mean())
                new_cy = int(cy + flow[cy:cy+h, cx:cx+w, 1].mean())
                new_x = int(new_cx - w / 2)
                new_y = int(new_cy - h / 2)
                new_box = [new_x, new_y, w, h]
                new_boxes1.append(new_box)

        obj_detector.draw_boxes(frame2, new_boxes1)


        cv.imshow('frame2', frame2)
        k = cv.waitKey(30) & 0xff

        frame1 = frame2
        results1 = results2