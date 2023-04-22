import os
import random
import shutil

from videos_to_frames import count_lines_in_files, save_video_frames_as_jpg
from annotations_rewriting import get_dimensions_videos, change_to_yolo_format
from annotations_rewriting import write_each_ann_to_single_file

def divide_dataset_into_train_and_val_sets(src_dir_labels, dst_dir_labels, 
                                           src_dir_images, dst_dir_images, division_percentage):
    labels_list = os.listdir(src_dir_labels)
    images_list = os.listdir(src_dir_images)

    num_files = len(labels_list) if len(labels_list) < len(images_list) else len(images_list)
    num_files_to_move = int(num_files * division_percentage)

    random_indices = random.sample(range(num_files), num_files_to_move)
    labels_to_be_moved_to_valset = [labels_list[i] for i in random_indices]
    images_to_be_moved_to_valset = [images_list[i] for i in random_indices]

    for file_name in labels_to_be_moved_to_valset:
        src_file_path = os.path.join(src_dir_labels, file_name)
        dst_file_path = os.path.join(dst_dir_labels, file_name)
        shutil.move(src_file_path, dst_file_path)

    for file_name in images_to_be_moved_to_valset:
        src_file_path = os.path.join(src_dir_images, file_name)
        dst_file_path = os.path.join(dst_dir_images, file_name)
        shutil.move(src_file_path, dst_file_path)


if __name__ == "__main__":    
    input_dir_with_annotations = "C:/Users/user/Music/annotations/challenge/annotations"
    input_dir_with_videos = "C:/Users/user/Downloads/train_videos/train_videos"
    output_dir_for_labels = "dataset/train/labels"
    output_dir_for_images = "dataset/train/images"
    dir_for_labels_valset = "dataset/val/labels"
    dir_for_images_valset = "dataset/val/images"

    dimensions = get_dimensions_videos(input_dir_with_videos)
    write_each_ann_to_single_file(input_dir_with_annotations, dimensions, output_dir_for_labels)

    lines_count = count_lines_in_files(input_dir_with_annotations)
    save_video_frames_as_jpg(input_dir_with_videos, lines_count, output_dir_for_images)

    divide_dataset_into_train_and_val_sets(output_dir_for_labels, dir_for_labels_valset, 
                                           output_dir_for_images, dir_for_images_valset, 0.15)



