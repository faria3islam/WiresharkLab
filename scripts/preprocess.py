import pandas as pd
import os

# Define the input and output file paths
pcap_file = '/home/kali/WiresharkLab/data/Traffic-Capture.pcap'
output_csv = "/home/kali/WiresharkLab/data/traffic_data.csv"

# Verify that the .pcap file exists
if not os.path.exists(pcap_file):
    raise FileNotFoundError(f"The .pcap file '{pcap_file}' was not found. Please provide the correct file.")

# Run tshark command to extract features from the pcap file
print("Extracting features from the .pcap file...")
os.system(
    f"tshark -r {pcap_file} -T fields -e frame.time -e ip.src -e ip.dst -e frame.len -e frame.protocols > {output_csv}"
)
print(f"Features successfully extracted and saved to '{output_csv}'.")

# Load the CSV file
print("Loading and preprocessing the data...")
data = pd.read_csv(output_csv, names=["time", "src_ip", "dst_ip", "length", "protocols"])

# Convert numerical data
data["length"] = pd.to_numeric(data["length"], errors='coerce')  # Convert 'length' to float safely

# **Log missing values before dropping them**
missing_data = data[data.isnull().any(axis=1)]
if not missing_data.empty:
    missing_log_file = "/home/kali/WiresharkLab/data/missing_data_log.csv"
    missing_data.to_csv(missing_log_file, index=False)
    print(f"Warning: {len(missing_data)} rows contain missing values. Logged in '{missing_log_file}'.")

# **Handle missing values instead of dropping them**
data.fillna({"src_ip": "UNKNOWN", "dst_ip": "UNKNOWN", "length": data["length"].median(), "protocols": "UNKNOWN"}, inplace=True)

# Normalize the 'length' column
data["length_normalized"] = data["length"] / data["length"].max()

# Save the preprocessed data
processed_csv = "/home/kali/WiresharkLab/data/preprocessed_data.csv"
data.to_csv(processed_csv, index=False)
print(f"Preprocessed data saved to '{processed_csv}'.")
