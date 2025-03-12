import pandas as pd
import os
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Define paths using os.path.join() for flexibility
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

# Initialize and train Isolation Forest for anomaly detection
print("Training Isolation Forest model...")
contamination_rate = 0.05  # Change if needed
model = IsolationForest(n_estimators=100, contamination=contamination_rate, random_state=42)
data["anomaly"] = model.fit_predict(features)

# Mark anomalies
data["anomaly_label"] = data["anomaly"].apply(lambda x: "Normal" if x == 1 else "Anomaly")

# Save the results to a CSV file
data.to_csv(RESULTS_CSV, index=False)
print(f"Anomaly detection results saved to '{RESULTS_CSV}'.")

# Visualize the results
plt.figure(figsize=(10, 6))
scatter = plt.scatter(data.index, data["length_normalized"], c=data["anomaly"], cmap="coolwarm", alpha=0.7)
plt.axhline(y=0.5, color="gray", linestyle="--", label="Threshold")
plt.xlabel("Packet Index")
plt.ylabel("Normalized Packet Length")
plt.title("Anomaly Detection in Network Traffic")
plt.legend()
plt.colorbar(scatter, label="Anomaly Score")  # Adds a color legend for anomalies
plt.grid(True)
plt.show()
