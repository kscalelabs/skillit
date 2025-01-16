
import matplotlib.pyplot as plt
import csv
import os




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
# # List of CSV files to plot
# csv_files = ["file1.csv", "file2.csv", "file3.csv"]

# # Initialize the plot
# plt.figure(figsize=(10, 6))

# # Loop through each file and plot its data
# for csv_file in csv_files:
#     timestamps = []
#     values = []
    
#     # Check if the file exists
#     if not os.path.exists(csv_file):
#         print(f"File not found: {csv_file}")
#         continue

#     # Read the CSV file
#     with open(csv_file, mode="r") as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header
#         for row in reader:
#             timestamps.append(float(row[0]))  # Convert timestamp to float
#             values.append(float(row[1]))  # Convert value to float

#     # Plot the data
#     plt.plot(timestamps, values, label=f"Data from {csv_file}")

# # Customize the plot
# plt.xlabel("Timestamp")
# plt.ylabel("Value")
# plt.title("Data from Multiple CSV Files")
# plt.legend()
# plt.grid(True)

# # Show the plot
# plt.show()





import matplotlib.pyplot as plt
import csv

# File to read from

for part in body:
    filename = part + ".csv"

    # Initialize lists to store data
    timestamps = []
    values = []

    # Read the data
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            timestamps.append(float(row[0]))  # Convert timestamp to float
            values.append(float(row[1]))  # Convert value to float

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, values, label="Streaming Data", color="blue")
    plt.xlabel("Timestamp")
    plt.ylabel("Position") 
    plt.title("Data from " + part)
    plt.legend()
    plt.grid(True)
    plt.show()

