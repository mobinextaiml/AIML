from ultralytics import YOLO

# Load a model
model = YOLO(r"C:\Users\DELL\Downloads\new\human_updated.pt")
# Use the model to detect objects
model.predict(
    source="rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/701/",
    show=True,
)
