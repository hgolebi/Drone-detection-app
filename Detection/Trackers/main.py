import torch
import cv2
from ultralytics import YOLO
from deep_sort_tracker import DeepSortTracker, SortTracker
import random

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

model = YOLO('yolov8l.pt')
model.to(device)

# Initialize the DeepSORT tracker
sort_tracker = DeepSortTracker()
# sort_tracker = SortTracker()

# Open the video file
video_in = cv2.VideoCapture("walk.mp4")
ret, frame = video_in.read()

cap_out = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc(*'mp4v'), video_in.get(cv2.CAP_PROP_FPS), (frame.shape[1], frame.shape[0]))

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(10)]

def yolo_box_to_box(box):
    return box[0], box[1], box[2] - box[0], box[3] - box[1]

detection_threshold = 0.5
while ret:
    [results] = model(frame)
    
    boxes = []
    scores = []
    for box, score, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
        score = score.item()
        box = [int(item) for item in box]
        if score > detection_threshold:
            boxes.append(yolo_box_to_box(box))
            scores.append(score)

    sort_tracker.update(boxes, scores, frame)

    for track in sort_tracker.tracks:
        x1, y1, x2, y2 = track.bbox

        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (colors[track.track_id % len(colors)]), 3)

    cap_out.write(frame)
    ret, frame = video_in.read()

video_in.release()
cap_out.release()
cv2.destroyAllWindows()

