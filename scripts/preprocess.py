import pandas as pd
import os

# Define the input and output file paths
pcap_file = "captured_traffic.pcap"
output_csv = "traffic_data.csv"

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
data["length"] = data["length"].astype(float)  # Ensure 'length' is float
data.dropna(inplace=True)  # Drop any rows with missing values

# Normalize the 'length' column
data["length_normalized"] = data["length"] / data["length"].max()

# Save the preprocessed data
processed_csv = "preprocessed_data.csv"
data.to_csv(processed_csv, index=False)
print(f"Preprocessed data saved to '{processed_csv}'.")
