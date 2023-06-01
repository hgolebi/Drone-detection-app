import cv2
import os

class VideoProcessor:
    def __init__(self):
        self.lines_count = []

    def count_lines_in_files(self, input_dir):
        """ Counts number of lines in an original annotations file - it corresponds to
        number of frames that can undergo a proccess of detection during model training """
        
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, "r") as file:
                num_lines = sum(1 for line in file)
            self.lines_count.append(num_lines)
        return self.lines_count

    def save_video_frames_as_jpg(self, input_dir_with_videos, lines_count, output_dir):
        """ Extracts frames from videos and saves them as jpgs """

        for filename, num_frames in zip(os.listdir(input_dir_with_videos), lines_count):
            video_path = os.path.join(input_dir_with_videos, filename)

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                cap.open(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            frame_interval = total_frames // num_frames

            for i in range(num_frames):
                if i % 10 == 0:
                    frame_index = i * frame_interval
                    frame = self.extract_frame(cap, frame_index)
                    if frame is not None:
                        output_path = os.path.join(output_dir, f"{filename[:-4]}_frame_{i:05d}.jpg")
                        cv2.imwrite(output_path, frame)

            cap.release()

    def extract_frame(self, cap, frame_index):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        return frame if ret else None