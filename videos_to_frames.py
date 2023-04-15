import cv2
import os

def count_lines_in_files(input_dir):
    lines_count = []

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "r") as file:
            num_lines = sum(1 for line in file)
        lines_count.append(num_lines)
    
    return lines_count


def save_video_frames_as_jpg(input_dir_with_videos, lines_count, output_dir):

    for filename, num_frames in zip(os.listdir(input_dir_with_videos), lines_count):
        print(filename, " running...")
        video_path = os.path.join(input_dir_with_videos, filename)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            cap.open(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # frame extraction interval
        frame_interval = total_frames // num_frames

        for i in range(num_frames):
            # frame index to extract
            frame_index = i * frame_interval

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

            ret, frame = cap.read()
            if not ret:
                continue

            output_path = os.path.join(output_dir, f"{filename[:-4]}_frame_{i:05d}.jpg")
            cv2.imwrite(output_path, frame)

        cap.release()
        # break

cv2.destroyAllWindows()
