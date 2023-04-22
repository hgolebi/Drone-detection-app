from ultralytics import YOLO

model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8s.pt")  # load a pretrained model

model.train(data="training_drones.yaml", epochs=3)  # train the model
# metrics = model.val()  # evaluate model performance on the validation set
results = model.predict(source="GOPR5842_005.mp4", save=True, save_txt=True)

# success = model.export(format="onnx")  # export the model to ONNX format