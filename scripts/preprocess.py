import pandas as pd
import os
import shutil  # For moving files
import subprocess

# Define the base directory where files should be stored
BASE_DIR = os.path.expanduser("~/WiresharkLab/data")

# Ensure the directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Define file paths within the /data/ directory
pcap_file = os.path.join(BASE_DIR, "Traffic-Capture.pcap")
output_csv = os.path.join(BASE_DIR, "traffic_data.csv")
missing_log_file = os.path.join(BASE_DIR, "missing_data_log.csv")
processed_csv = os.path.join(BASE_DIR, "preprocessed_data.csv")

# Function to move a received CSV file into the /data/ directory
def move_to_data_folder(filename):
    if os.path.exists(filename):
        new_location = os.path.join(BASE_DIR, os.path.basename(filename))
        shutil.move(filename, new_location)
        print(f"Moved '{filename}' to '{new_location}'")
        return new_location
    return filename

# Example: Move a received CSV to the /data/ folder (if applicable)
received_csv = "received_traffic_data.csv"  # Example filename of received data
if os.path.exists(received_csv):
    output_csv = move_to_data_folder(received_csv)  # Move it and update output_csv path

# Verify that the .pcap file exists before processing
if not os.path.exists(pcap_file):
    raise FileNotFoundError(f"The .pcap file '{pcap_file}' was not found. Please provide the correct file.")

# Check if tshark is installed
if subprocess.run(["which", "tshark"], capture_output=True).returncode != 0:
    raise EnvironmentError("Error: 'tshark' is not installed. Install it using 'sudo apt install tshark'.")

# Run tshark command to extract features from the pcap file
print("Extracting features from the .pcap file...")
try:
    subprocess.run(
        ["tshark", "-r", pcap_file, "-T", "fields",
         "-e", "frame.time", "-e", "ip.src", "-e", "ip.dst", "-e", "frame.len", "-e", "frame.protocols"],
        stdout=open(output_csv, "w"), stderr=subprocess.PIPE, check=True
    )
    print(f"Features successfully extracted and saved to '{output_csv}'.")
except subprocess.CalledProcessError as e:
    raise RuntimeError(f"tshark command failed: {e.stderr.decode()}")

# Load the CSV file
print("Loading and preprocessing the data...")
data = pd.read_csv(output_csv, names=["time", "src_ip", "dst_ip", "length", "protocols"])

# Convert numerical data safely
data["length"] = pd.to_numeric(data["length"], errors='coerce')

# Log missing values before handling them
missing_data = data[data.isnull().any(axis=1)]
if not missing_data.empty:
    missing_data.to_csv(missing_log_file, index=False)
    print(f"Warning: {len(missing_data)} rows contain missing values. Logged in '{missing_log_file}'.")

# Handle missing values
data.fillna({"src_ip": "UNKNOWN", "dst_ip": "UNKNOWN",
             "length": data["length"].median(), "protocols": "UNKNOWN"}, inplace=True)

# Prevent zero division error in normalization
length_max = data["length"].max()
if length_max > 0:
    data["length_normalized"] = data["length"] / length_max
else:
    print("Warning: Maximum length is zero, skipping normalization.")
    data["length_normalized"] = 0

# Save the preprocessed data
data.to_csv(processed_csv, index=False)
print(f"Preprocessed data saved to '{processed_csv}'.")
