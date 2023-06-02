from videos_to_frames import VideoProcessor
from annotations_rewriting import AnnotationsRewriter
from dataset_division import DatasetDivider

class DatasetPreprocessor:
    def __init__(self, input_dir_with_annotations, input_dir_with_videos,
                 output_dir_for_labels, output_dir_for_images,
                 dir_for_labels_valset, dir_for_images_valset, division_percentage):
        self.input_dir_with_annotations = input_dir_with_annotations
        self.input_dir_with_videos = input_dir_with_videos
        self.output_dir_for_labels = output_dir_for_labels
        self.output_dir_for_images = output_dir_for_images
        self.dir_for_labels_valset = dir_for_labels_valset
        self.dir_for_images_valset = dir_for_images_valset
        self.division_percentage = division_percentage

    def run(self):
        self._process_annotations()
        self._process_videos()
        self._divide_dataset()

    def _process_annotations(self):
        ann_rewriter = AnnotationsRewriter()
        dimensions = ann_rewriter.get_dimensions_videos(self.input_dir_with_videos)
        ann_rewriter.write_each_ann_to_single_file(self.input_dir_with_annotations, dimensions,
                                                   self.output_dir_for_labels)

    def _process_videos(self):
        vid_processor = VideoProcessor()
        lines_count = vid_processor.count_lines_in_files(self.input_dir_with_annotations)
        vid_processor.save_video_frames_as_jpg(self.input_dir_with_videos, lines_count,
                                               self.output_dir_for_images)

    def _divide_dataset(self):
        data_divider = DatasetDivider(self.output_dir_for_labels, self.dir_for_labels_valset,
                                      self.output_dir_for_images, self.dir_for_images_valset,
                                      self.division_percentage)
        data_divider.divide_dataset_into_train_and_val_sets()


if __name__ == "__main__":
    input_dir_with_annotations = "annotations/challenge/annotations"
    input_dir_with_videos = "Downloads/train_videos/train_videos"
    output_dir_for_labels = "dataset/train/labels"
    output_dir_for_images = "dataset/train/images"
    dir_for_labels_valset = "dataset/val/labels"
    dir_for_images_valset = "dataset/val/images"
    division_percentage = 0.15

    preprocessor = DatasetPreprocessor(input_dir_with_annotations, input_dir_with_videos,
                                       output_dir_for_labels, output_dir_for_images,
                                       dir_for_labels_valset, dir_for_images_valset, division_percentage)
    preprocessor.run()
