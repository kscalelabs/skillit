import csv
import random
import time
import pykos

body = {
    'l_shoulder' : 14,
    'l_rotator' : 15,
    'l_elbow' : 16,
    'r_shoulder' : 13,
    'r_elbow' : 11,
    'r_rotator' : 12,
    'l_ankle' : 6,
    'l_knee' : 7,
    'l_thigh' : 8,
    'l_hamstring' : 9,
    'l_hip' : 10,
    'r_ankle' : 1,
    'r_knee' : 2,
    'r_thigh' : 3,
    'r_hamstring' : 4,
    'r_hip' : 5
}

kos = pykos.KOS(ip='10.33.13.110')
# File to store data

for part in body:

    filename = part + ".csv"

    # Initialize the CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Value"])  # Add a header

# Simulating a data stream
try:
    initial_time = time.time()
    while True:

        for part in body:
        # Simulate data coming in
            timestamp = time.time() - initial_time # Current timestamp
            value = kos.actuator.get_actuators_state([body[part]])[0].position
            # value = 0
            filename = part + ".csv"
            # Append to CSV
            with open(filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, value])

        print(f"Stored: {timestamp}, {value}")
        time.sleep(.01)  # Simulate data rate
except KeyboardInterrupt:
    print("Stopped data collection.")
