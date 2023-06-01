import random
import shutil
import os

class DatasetDivider:
    """ Takes dataset with labels and images and divides it 
    into two datasets: train set and validation set """

    def __init__(self, src_dir_labels, dst_dir_labels, 
                 src_dir_images, dst_dir_images, division_percentage):
        self.src_dir_labels = src_dir_labels
        self.dst_dir_labels = dst_dir_labels
        self.src_dir_images = src_dir_images
        self.dst_dir_images = dst_dir_images
        self.division_percentage = division_percentage

    def divide_dataset_into_train_and_val_sets(self):
        labels_list = os.listdir(self.src_dir_labels)
        images_list = os.listdir(self.src_dir_images)

        num_files = len(labels_list) if len(labels_list) < len(images_list) else len(images_list)
        num_files_to_move = int(num_files * self.division_percentage)

        random_indices = random.sample(range(num_files), num_files_to_move)
        labels_to_be_moved_to_valset = [labels_list[i] for i in random_indices]
        images_to_be_moved_to_valset = [images_list[i] for i in random_indices]

        self.move_files_to_valset(labels_to_be_moved_to_valset, 
                                  self.src_dir_labels, self.dst_dir_labels)
        self.move_files_to_valset(images_to_be_moved_to_valset, 
                                  self.src_dir_images, self.dst_dir_images)

    def move_files_to_valset(self, file_list, src_dir, dst_dir):
        for file_name in file_list:
            src_file_path = os.path.join(src_dir, file_name)
            dst_file_path = os.path.join(dst_dir, file_name)
            shutil.move(src_file_path, dst_file_path)
