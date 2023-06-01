from videos_to_frames import VideoProcessor
from annotations_rewriting import AnnotationsRewriter
from dataset_division import DatasetDivider

if __name__ == "__main__":    
    input_dir_with_annotations = "annotations/challenge/annotations"
    input_dir_with_videos = "Downloads/train_videos/train_videos"
    output_dir_for_labels = "dataset/train/labels"
    output_dir_for_images = "dataset/train/images"
    dir_for_labels_valset = "dataset/val/labels"
    dir_for_images_valset = "dataset/val/images"

    ann_rewirter = AnnotationsRewriter()
    dimensions = ann_rewirter.get_dimensions_videos(input_dir_with_videos)
    ann_rewirter.write_each_ann_to_single_file(input_dir_with_annotations, 
                                               dimensions, output_dir_for_labels)

    vid_processor = VideoProcessor()
    lines_count = vid_processor.count_lines_in_files(input_dir_with_annotations)
    vid_processor.save_video_frames_as_jpg(input_dir_with_videos, lines_count, output_dir_for_images)

    data_divider = DatasetDivider(output_dir_for_labels, dir_for_labels_valset, 
                                    output_dir_for_images, dir_for_images_valset, 0.15)



