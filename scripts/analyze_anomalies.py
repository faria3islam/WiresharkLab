import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Load the preprocessed data
preprocessed_data_file = "/home/kali/WiresharkLab/data/preprocessed_data.csv"
data = pd.read_csv(preprocessed_data_file)

# Ensure the necessary columns are available
if "length_normalized" not in data.columns:
    raise ValueError(f"Column 'length_normalized' not found in the file '{preprocessed_data_file}'.")

# Use only the normalized length feature for anomaly detection
features = data[["length_normalized"]].values

# Initialize and train Isolation Forest for anomaly detection
print("Training Isolation Forest model...")
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
data["anomaly"] = model.fit_predict(features)

# Mark anomalies
data["anomaly_label"] = data["anomaly"].apply(lambda x: "Normal" if x == 1 else "Anomaly")

# Save the results to a CSV file
results_csv = "/home/kali/WiresharkLab/results/anomaly_detection_results.csv"
data.to_csv(results_csv, index=False)
print(f"Anomaly detection results saved to '{results_csv}'.")

# Visualize the results
plt.figure(figsize=(10, 6))
plt.scatter(data.index, data["length_normalized"], c=data["anomaly"], cmap="coolwarm", label="Anomaly")
plt.axhline(y=0.5, color="gray", linestyle="--", label="Threshold")
plt.xlabel("Packet Index")
plt.ylabel("Normalized Packet Length")
plt.title("Anomaly Detection in Network Traffic")
plt.legend()
plt.grid(True)
plt.show()
