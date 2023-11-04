from confluent_kafka import Producer
import cv2
import time
import csv
from datetime import datetime

# Kafka and camera configurations
KAFKA_BROKER = "localhost:9092"  # Change this to the appropriate Kafka broker address
KAFKA_TOPIC_PREFIX = "camera_streaming"

cameras = {
    101: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/101/",
    202: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/201/",
    303: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/301/",
    404: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/401/",
    505: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/501/",
    606: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/601/",
    707: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/701/",
    808: "rtsp://admin:admin12345@192.168.1.245:554/Streaming/Channels/801/",
}


# Kafka producer configuration
def get_kafka_producer():
    config = {"bootstrap.servers": KAFKA_BROKER}
    return Producer(config)


# Function for writing events to a CSV file
def write_to_csv(event, camera_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = f"events_camera_{camera_id}.csv"
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([event, timestamp])


# Function to read video streams from camera sources and publish to Kafka
def send_camera_streams():
    producer = get_kafka_producer()

    for camera_id, video_file in cameras.items():
        cap = cv2.VideoCapture(video_file)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

            topic = KAFKA_TOPIC_PREFIX + str(camera_id)

            producer.produce(topic, value=frame_bytes)
            producer.flush()  # Ensuring delivery to the Kafka broker
            time.sleep(1)  # Adjust the time interval as needed

            # Writing events to CSV
            event = f"Event detected from camera {camera_id}"
            write_to_csv(event, camera_id)

        cap.release()


if __name__ == "__main__":
    send_camera_streams()
