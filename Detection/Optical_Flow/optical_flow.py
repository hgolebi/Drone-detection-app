import numpy as np
import cv2 as cv


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
    ret, frame1 = cap.read()
    
    while True:
        ret, frame2 = cap.read()
        flow = of.calculate_flow(frame1, frame2)
        flow_map = of.map_flow(flow)
        cv.imshow('frame2', flow_map)
        k = cv.waitKey(30) & 0xff
        frame1 = frame2
    