from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')

if __name__ == '__main__': # can khi chay bang GPU
    model.train(data='dataset.yaml', epochs=40, imgsz=640, batch=16, optimizer='SGD', workers=1)
    metrics = model.val()