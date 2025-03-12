import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scapy.all import sniff
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

# Initialize the anomaly detection model
print("Initializing the Isolation Forest model...")
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

# Initialize storage for live packet analysis
packets_data = []

# Set up Matplotlib for real-time visualization
fig, ax = plt.subplots()
sc = ax.scatter([], [], c=[], cmap="coolwarm", label="Anomalies")
ax.set_xlim(0, 50)  # Show the last 50 packets
ax.set_ylim(0, 1)  # Normalized length range
ax.set_xlabel("Packet Index")
ax.set_ylabel("Normalized Packet Length")
ax.set_title("Live Network Traffic Anomaly Detection")
ax.legend()
plt.grid(True)

def process_packet(packet):
    """Process a single captured packet and update data."""
    global packets_data

    # Extract packet features
    length = len(packet)
    protocol = packet.name  # This is unused in visualization but can be logged

    # Append packet data
    packets_data.append({"length": length})

    # Convert to DataFrame
    df = pd.DataFrame(packets_data)

    # Normalize 'length' column
    df["length_normalized"] = df["length"] / df["length"].max()

    # Keep only the last 50 packets for visualization
    if len(df) > 50:
        df = df.iloc[-50:]

    # Perform anomaly detection (only if we have enough data)
    if len(df) > 10:
        features = df[["length_normalized"]].values
        anomalies = model.fit_predict(features)
        df["anomaly"] = anomalies

        # Print latest packet's anomaly status
        anomaly_status = "Anomaly" if anomalies[-1] == -1 else "Normal"
        print(f"Packet: Length={length}, Status={anomaly_status}")

        # Update scatter plot data
        sc.set_offsets(np.c_[range(len(df)), df["length_normalized"]])
        sc.set_array(df["anomaly"])  # Color by anomaly status

def update(_):
    """Update function for animation loop."""
    return sc,

# Start real-time packet sniffing
print("Starting live packet capture... (Press Ctrl+C to stop)")
ani = animation.FuncAnimation(fig, update, interval=1000)  # Update every second
sniff(prn=process_packet, store=False, count=50)  # Capture 50 packets

plt.show()  # Show the real-time plot
