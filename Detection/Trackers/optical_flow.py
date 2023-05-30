import numpy as np
import cv2 as cv
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
            self.curr_frame = self.convert_frame_to_gray(frame)
            # TODO refactor flow call
            flow = self.calculate_flow(self.last_frame, self.curr_frame)
            new_bboxes = self.get_bbox_from_flow(flow)
            self.compare_boxes(new_bboxes, bboxes)
            print(self.tracks)
        else:
            self.last_frame = self.convert_frame_to_gray(frame)
    
    def get_bbox_from_flow(self, flow_map):
        """ return xywh bbox from flow """
        magnitude, _ = cv.cartToPolar(flow_map[..., 0], flow_map[..., 1])
        filtered_magnitude = magnitude > 5
        contours, _ = cv.findContours(filtered_magnitude.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        bounding_boxes = np.array([cv.boundingRect(contour) for contour in contours])
        if bounding_boxes.ndim == 2:
            bounding_boxes = bounding_boxes[np.all(bounding_boxes>10, axis=1)]
            print(bounding_boxes)
        
        # bounding_boxes = [(x1, y1, x1+x2, y1+y2) for (x1, y1, x2, y2) in bounding_boxes]
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
                    if track.last_updated < 3:
                        new_tracks.append(track)
            
            self.tracks = sorted(new_tracks, key=lambda t: t.track_id)
    
    def convert_frame_to_gray(self, frame):
        """converts frame from RGB to GRAY color"""
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    def calculate_flow(self, frame_prev, frame_next):
        """calculates optical flow based on two RGB frames"""
        # frame_prev = self.convert_frame_to_gray(frame_prev)
        # frame_next = self.convert_frame_to_gray(frame_next)
        return cv.calcOpticalFlowFarneback(frame_prev, frame_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # def get_new_box_with_optical_flow(self, box, flow, prev_boxes=False):
    #     """calculates new box position using optical flow"""
    #     cx, cy, w, h = map(int, box[:4])
    #     new_cx = int(cx + flow[cy:cy+h, cx:cx+w, 0].mean())
    #     new_cy = int(cy + flow[cy:cy+h, cx:cx+w, 1].mean())
    #     new_x = int(new_cx - w / 2)
    #     new_y = int(new_cy - h / 2)
    #     new_box = [new_x, new_y, w, h]
    #     return new_box

    # def map_flow(self, flow):
    #     """maps flow on rgb frame with shape as input frames"""
    #     mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
    #     hsv = np.zeros(shape=(*ang.shape, 3), dtype=np.uint8)
    #     hsv[..., 0] = ang*180/np.pi/2
    #     hsv[..., 1] = 255
    #     hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    #     bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    #     return bgr
    
    
    

# if __name__ == '__main__':
#     cap = cv.VideoCapture(cv.samples.findFile("./walk.mp4"))

#     of = OpticalFlow()
#     ret, frame1 = cap.read()
    
#     while True:
#         ret, frame2 = cap.read()
#         flow = of.calculate_flow(frame1, frame2)
#         print(of.get_bbox_from_flow(flow))
#         # flow_map = of.map_flow(flow)
#         # cv.imshow('frame2', flow_map)
#         # k = cv.waitKey(30) & 0xff
#         frame1 = frame2
    
    