import csv
from datetime import datetime

# Function for ML-based event segregation and writing to CSV
def ml_event_segregation_and_store(event, detected_objects):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Write the event, timestamp, and detected objects to a CSV file
    with open("events.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([event, timestamp, detected_objects])

# Function to segregate events class-wise
def segregate_events_class_wise(csv_file):
    with open(csv_file, mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if present

        class_files = {}  # Dictionary to store file handles for each class
        for row in csv_reader:
            event, timestamp, detected_objects = row[0], row[1], row[2]
            for obj in detected_objects.split(","):
                obj = obj.strip()
                class_file = class_files.get(obj)
                if not class_file:
                    class_file = open(f"{obj}_events.csv", mode="a", newline="")
                    class_files[obj] = class_file
                    class_file_writer = csv.writer(class_file)
                    class_file_writer.writerow(
                        ["event_description", "timestamp"]
                    )  # Write header for each class file
                else:
                    class_file_writer = csv.writer(class_file)
                class_file_writer.writerow([event, timestamp])

        # Close all class-wise files
        for file in class_files.values():
            file.close()

# Call the function for each event from the model
ml_event_segregation_and_store("person spotted near the entrance", "person")
ml_event_segregation_and_store("suspicious vehicle in parking lot", "vehicle")
ml_event_segregation_and_store("suspicious person carrying a bag", "person")

# After storing all events, call the segregate function
segregate_events_class_wise("events.csv")
