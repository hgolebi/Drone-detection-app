from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def train_model(self, data_file, epochs, img_size):
        self.model.train(data=data_file, epochs=epochs, imgsz=img_size)

    def evaluate_model(self):
        metrics = self.model.val()
        return metrics

    def predict_objects(self, source, save_results=True, save_txt=True):
        results = self.model.predict(source=source, save=save_results, save_txt=save_txt)
        return results


if __name__ == "__main__":
    model_path = "yolov8s.pt" # pretrained model
    model_path = "models/best.pt" # pretrained model which has already gone through some of our own training
    training_data_file = "training_drones.yaml"

    detector = ObjectDetector(model_path)
    detector.train_model(training_data_file, 3, 640)
    metrics = detector.evaluate_model()
    results = detector.predict_objects("GOPR5842_005.mp4", save_results=True, save_txt=True)
