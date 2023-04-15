import cv2
import os

def get_dimensions_videos(dir_with_videos):
    dimensions = []

    if os.path.exists("dimensions.txt"):
        with open("dimensions.txt", 'r') as file:
            lines = file.readlines()
            for line in lines[:-1]:
                width, height = line.strip().split(", ")
                dimensions.append((float(width), float(height)))
    else:
        for idx, filename in enumerate(os.listdir(dir_with_videos)):
            vid = cv2.VideoCapture(filename)
            if not vid.isOpened():
                vid.open(os.path.join(dir_with_videos, filename))

            height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            dimensions.append((width, height))
            with open("dimensions.txt", 'a') as file:
                dim = f"{width}, {height}\n" if (idx+1 < len(os.listdir(dir_with_videos))) \
                    else f"{width}, {height}"
                file.write(dim)

            vid.release()

    return dimensions


def change_to_yolo_format(line, width, height):
    drones_captured = []
    values = line.strip().split(' ')
    # print(values)
    # values = [abs(int(x)) for x in values]
    # print(values)
    if len(values) > 7:
        drones_captured.append(values[1:6])
        drones_captured.append(values[6:-1])
    else:
        drones_captured.append(values[1:-1])
    
    new_anns = []
    for drone in drones_captured:
        if values[1] != '0':
            drone[0] = '0'
            drone[1] = str((int(drone[1]) + (int(drone[3])/2)) / width)
            drone[2] = str((int(drone[2]) - (int(drone[4])/2)) / height)
            drone[3] = str(int(drone[3]) / width)
            drone[4] = str(int(drone[4]) / height)
            new_anns.append(" ".join(drone))
        else:
            new_anns.append("")
    return new_anns


def write_each_ann_to_single_file(input_dir_with_annotations, dimensions, output_dir):
    for filename, dimension in zip(os.listdir(input_dir_with_annotations), dimensions):
        print(filename, " running...")
        file_path = os.path.join(input_dir_with_annotations, filename)
        width, height = dimension

        with open(file_path, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            frame_num = int(line.split(" ")[0])
            output_path = output_dir + "/" + f"{filename[:-4]}_frame_{frame_num:05d}.txt"
            with open(output_path, 'w') as new_file:
                new_lines = change_to_yolo_format(line, width, height)
                for idx, new_line in enumerate(new_lines):
                    if idx+1 < len(new_lines):
                        new_line += "\n"
                    new_file.write(new_line)