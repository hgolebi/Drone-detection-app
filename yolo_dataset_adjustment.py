from videos_to_frames import count_lines_in_files, save_video_frames_as_jpg
from annotations_rewriting import get_dimensions_videos, change_to_yolo_format
from annotations_rewriting import write_each_ann_to_single_file


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