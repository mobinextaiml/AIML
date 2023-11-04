from confluent_kafka import Consumer, KafkaException
from ultralytics import YOLO
import csv
import time

# Define Kafka and RabbitMQ configurations
KAFKA_BROKER = "localhost:9092"  # Change this to the appropriate Kafka broker address
KAFKA_TOPIC_PREFIX = "camera_streaming"

# Define the YOLO models for each camera
models = {
    101: YOLO("human_updated.pt"),
    202: YOLO("human_updated.pt"),
    303: YOLO("human_updated.pt"),
    404: YOLO("human_updated.pt"),
    505: YOLO("human_updated.pt"),
    606: YOLO("human_updated.pt"),
    707: YOLO("human_updated.pt"),
    807: YOLO("human_updated.pt"),
}


# Function to write events to a CSV file
def write_to_csv(event, camera_id):
    file_name = f"events_camera_{camera_id}.csv"
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([event, time.ctime()])


# Function to process the camera stream through all the models
def process_camera_stream(camera_id):
    consumer = get_kafka_consumer(camera_id)
    consumer.subscribe([f"{KAFKA_TOPIC_PREFIX}{camera_id}"])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            frame = msg.value().decode("utf-8")
            print(f"Processing frame {frame} from Camera {camera_id}...")

            # Example event creation and storage
            yolo_model = models[camera_id]
            event = yolo_model.predict(source=frame, save=False, show=False)
            print(f"Storing event '{event}' in database...")
            write_to_csv(event, camera_id)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


if __name__ == "__main__":
    process_camera_stream()
