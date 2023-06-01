import random
import shutil
import os
import unittest
from dataset_division import DatasetDivider
from unittest.mock import MagicMock


class DatasetDividerTests(unittest.TestCase):

    def setUp(self):
        self.src_dir_labels = "src/labels"
        self.dst_dir_labels = "dst/labels"
        self.src_dir_images = "src/images"
        self.dst_dir_images = "dst/images"
        self.division_percentage = 0.2
        os.makedirs(self.src_dir_labels, exist_ok=True)
        os.makedirs(self.src_dir_images, exist_ok=True)
        os.makedirs(self.dst_dir_labels, exist_ok=True)
        os.makedirs(self.dst_dir_images, exist_ok=True)
        self.divider = DatasetDivider(self.src_dir_labels, self.dst_dir_labels, 
                                       self.src_dir_images, self.dst_dir_images, 
                                       self.division_percentage)

    def tearDown(self):
        shutil.rmtree(self.src_dir_labels)
        shutil.rmtree(self.src_dir_images)
        shutil.rmtree(self.dst_dir_labels, ignore_errors=True)
        shutil.rmtree(self.dst_dir_images, ignore_errors=True)
    
    def test_divide_dataset_into_train_and_val_sets(self):
        labels_files = ["label1.txt", "label2.txt", "label3.txt", "label4.txt"]
        for file_name in labels_files:
            file_path = os.path.join(self.src_dir_labels, file_name)
            open(file_path, "w").close()

        images_files = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg"]
        for file_name in images_files:
            file_path = os.path.join(self.src_dir_images, file_name)
            open(file_path, "w").close()
        random.seed(123)
        random_indices = [1, 3]  # indicies 'drawn' to be moved

        random.sample = MagicMock(return_value=random_indices)

        self.divider.divide_dataset_into_train_and_val_sets()

        self.assertTrue(os.path.exists(os.path.join(self.dst_dir_labels, "label2.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir_labels, "label4.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir_images, "image2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir_images, "image4.jpg")))


    def test_move_files_to_valset(self):
        files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]
        for file_name in files:
            file_path = os.path.join(self.src_dir_labels, file_name)
            open(file_path, "w").close()

        self.divider.move_files_to_valset(files[:2], self.src_dir_labels, self.dst_dir_labels)

        for file_name in files[:2]:
            dst_file_path = os.path.join(self.dst_dir_labels, file_name)
            self.assertTrue(os.path.exists(dst_file_path))


if __name__ == '__main__':
    unittest.main()
