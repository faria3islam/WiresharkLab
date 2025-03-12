import pandas as pd
import os
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import numpy as np

# Define paths
BASE_DIR = os.path.expanduser("~/WiresharkLab")
DATA_FILE = os.path.join(BASE_DIR, "data/preprocessed_data.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
RESULTS_CSV = os.path.join(RESULTS_DIR, "anomaly_detection_results.csv")

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Load the preprocessed data
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Error: Preprocessed data file '{DATA_FILE}' not found!")

print("Loading preprocessed data...")
data = pd.read_csv(DATA_FILE)

# Ensure required column exists
if "length_normalized" not in data.columns:
    raise ValueError(f"Error: Column 'length_normalized' not found in '{DATA_FILE}'.")

# Ensure data is not empty
if data.empty:
    raise ValueError("Error: Preprocessed data is empty! Cannot perform anomaly detection.")

# Use only the normalized length feature
features = data[["length_normalized"]].values

# Dynamically determine contamination (percentage of anomalies)
contamination_rate = max(0.1, min(0.1, 1.0 / len(data)))

# Train Isolation Forest
print(f"Training Isolation Forest model with contamination={contamination_rate:.4f}...")
model = IsolationForest(n_estimators=100, contamination=contamination_rate, random_state=42)

# **Fix: Fit the model before calling decision_function**
data["anomaly"] = model.fit_predict(features)
data["anomaly_score"] = model.decision_function(features)  # Get anomaly scores **AFTER FITTING**

# Convert anomalies to labels
data["anomaly_label"] = data["anomaly"].apply(lambda x: "Normal" if x == 1 else "Anomaly")

# Save the results
data.to_csv(RESULTS_CSV, index=False)
print(f"Anomaly detection results saved to '{RESULTS_CSV}'.")

# Plot anomalies with better visualization
plt.figure(figsize=(12, 6))

# Use log scaling to improve visibility if data is highly skewed
plt.yscale("log")

# Scatter plot with color-coded anomalies
scatter = plt.scatter(data.index, data["length_normalized"], c=data["anomaly_score"], cmap="RdYlGn", alpha=0.7)
plt.colorbar(scatter, label="Anomaly Score")

# Adjust threshold dynamically
threshold = np.percentile(data["anomaly_score"], 5)  # Set threshold at the bottom 5%
plt.axhline(y=threshold, color="black", linestyle="--", label=f"Anomaly Threshold ({threshold:.4f})")

plt.xlabel("Packet Index")
plt.ylabel("Normalized Packet Length (Log Scale)")
plt.title("Anomaly Detection in Network Traffic")
plt.legend()
plt.grid(True)
plt.show()
