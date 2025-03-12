from scapy.all import sniff
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

# Initialize the anomaly detection model (Isolation Forest)
print("Initializing the Isolation Forest model...")
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

# Initialize storage for live packet analysis
packets_data = []

def process_packet(packet):
    """Process a single captured packet."""
    global packets_data
    
    # Extract features: packet length and protocol
    length = len(packet)
    protocol = packet.name

    # Add packet data to the list
    packets_data.append({"length": length, "protocol": protocol})

    # Convert to DataFrame for real-time analysis
    df = pd.DataFrame(packets_data)

    # Normalize length
    df["length_normalized"] = df["length"].astype(float) / df["length"].max()

    # Perform anomaly detection only if enough packets are captured
    if len(df) > 10:  # Require at least 10 packets for analysis
        features = df[["length_normalized"]].values
        anomalies = model.fit_predict(features)

        # Print the latest packet's anomaly status
        anomaly_status = "Anomaly" if anomalies[-1] == -1 else "Normal"
        print(f"Packet: Length={length}, Protocol={protocol}, Status={anomaly_status}")


# Start live capture on the default network interface
print("Starting live packet capture... (Press Ctrl+C to stop)")
sniff(prn=process_packet, store=False, count=50)  # Adjust count or remove it for continuous capture
