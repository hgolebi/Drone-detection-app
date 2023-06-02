import cv2
import os

class AnnotationsRewriter:
    def __init__(self):
        self.dimensions = []

    def get_dimensions_videos(self, dir_with_videos, dimensions_file="dimensions.txt"):
        """ Extracts the dimensions of all videos from the 
        dataset of videos and saves them to a file """

        if os.path.exists(dimensions_file):
            self.load_dimensions_from_file(dimensions_file)
        else:
            self.calculate_dimensions(dir_with_videos)
            self.save_dimensions_to_file(dimensions_file)
        return self.dimensions

    def load_dimensions_from_file(self, dimensions_file):
        with open(dimensions_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                width, height = line.strip().split(", ")
                self.dimensions.append((float(width), float(height)))

    def calculate_dimensions(self, dir_with_videos):
        for idx, filename in enumerate(os.listdir(dir_with_videos)):
            vid = cv2.VideoCapture(filename)
            if not vid.isOpened():
                vid.open(os.path.join(dir_with_videos, filename))

            width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.dimensions.append((width, height))

            vid.release()

    def save_dimensions_to_file(self, dimensions_file):
        with open(dimensions_file, 'a') as file:
            for idx, dim in enumerate(self.dimensions):
                width, height = dim
                if idx+1 < len(self.dimensions):
                    file.write(f"{width}, {height}\n")
                else:
                    file.write(f"{width}, {height}")

    def change_to_yolo_format(self, line, width, height):
        """ Takes a single line from file with annotations and converts it 
        to the yolo format so that the coordinates of an object looks like this: 
        x, y (the center of the object) and width, height (of the object).
        Then the values are normalized to the dimensions of the video - 
        get_dimensions_videos method is needed """

        drones_captured = []
        values = line.strip().split(' ')
        if len(values) > 2:
            drone_values = []
            for value in values[2:]:
                if value == 'drone':
                    drones_captured.append(drone_values)
                    drone_values = []
                    continue
                drone_values.append(value)

        new_anns = []
        for drone in drones_captured:
            if values[1] != '0':
                drone = self.convert_drone_coordinates(drone, width, height)

                drone.insert(0, '0')
                new_anns.append(" ".join(drone))
            else:
                new_anns.append("")
        return new_anns

    def convert_drone_coordinates(self, drone, width, height):
        drone[0] = str((int(drone[0]) + (int(drone[2]) / 2)) / width)
        drone[1] = str((int(drone[1]) + (int(drone[3]) / 2)) / height)
        drone[2] = str(int(drone[2]) / width)
        drone[3] = str(int(drone[3]) / height)
        
        for idx, dr in enumerate(drone):
            if float(dr) < 0:
                drone[idx] = '0.0'
        
        return drone

    def write_each_ann_to_single_file(self, input_dir_with_annotations, dimensions, output_dir):
        """ Takes each line from original annotations, changes 
        to yolo format and saves to a seperate txt file """

        for filename, dimension in zip(os.listdir(input_dir_with_annotations), dimensions):
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            print(filename, " running...")
            file_path = os.path.join(input_dir_with_annotations, filename)
            width, height = dimension

            with open(file_path, "r") as f:
                lines = f.readlines()

            for idx, line in enumerate(lines):
                if idx % 10 == 0:
                    frame_num = int(line.split(" ")[0])
                    output_path = output_dir + "/" + f"{filename[:-4]}_frame_{frame_num:05d}.txt"
                    with open(output_path, 'w') as new_file:
                        new_lines = self.change_to_yolo_format(line, width, height)
                        for idx, new_line in enumerate(new_lines):
                            if idx + 1 < len(new_lines):
                                new_line += "\n"
                            new_file.write(new_line)