# Network Traffic Analysis - Prediction & Monitoring

## Objective:
- Analyze traffic patterns using Wireshark
- Predict anomalies indicating potential threats using Python TensorFlow
- Monitor and analyze network data for ongoing security.

## Pre-requisites: 
- Familiarity with Kali Linux
- Familiarity with Wireshark is a plus
- Familiarity with Python is a plus

## Materials Needed: 
- Kali Linux Virtual Environment
- Wireshark (should already be pre installed in Kali Linux)
- Tshark (should already be pre installed in Kali Linux)
- Python 3 and libraries numpy, pandas, matplotlib, scikit-learn, and scapy

## Lab Description: 
- In this lab, participants will simulate network traffic analysis using Wireshark within a controlled environment (Kali Linux) to then export as a .pcap file. 
- Participants will then simulate predictive anomaly detection using machine learning.

## Duration: 
- 30-45 minutes.

## Step-by-Step Instructions
### Lab Set Up:
- Launch Kali Linux settings on your virtual machine
- Setup Bridged Adaptor Network

![Screenshot of Bridged Adaptor settings](https://github.com/user-attachments/assets/885583ce-9c5a-49c6-93a4-65b0b59226a4)

- IP Addressing: Run the following command and keep note of the assigned IP.
```
ifconfig
```
- Make sure system is updated:
```
sudo apt update
```
- Clone Github repository:
```
git clone https://github.com/faria3islam/WiresharkLab.git
```
- Change directory into WiresharkLab
```
cd WiresharkLab
```
- Install Wireshark, Python, and Dependencies as needed
- To save time, check versions first (ex. wireshark --v or python3 --version)
```
sudo apt install wireshark -y
sudo apt install tshark -y
sudo apt install python3 python3-pip -y
pip install -r requirements.txt
```

### Lab Activity 1 - Password Capture Using Wireshark:
In this activity, participants will use Wireshark filters to find passwords used on vulnerable sites in a virtual environment. **Must be done in virtual environment**.
**Steps:**
- Launch Wireshark on Kali Linux
- Choose a network to capture (likely eth0)
- Launch a browser (firefox)
- Using a vulnerable web page, enter login info (link provided)
- Stop capturing packets.
- Filter down the packets to POST and GET packets
- Investigate the packets to find the password used.
- **Deliverable:** Screenshot of Wireshark capture after filtering and finding password

![Screenhot of example deliverable](https://github.com/user-attachments/assets/20e2d7c3-982e-45ce-bcfa-67653ef471cf)

### Lab Activity 2 - Predicting Anomalies - Indicating Potential Threats:
In this activity, participants get hands-on experience with network security techniques, combining packet capture, data preprocessing, and AI-based anomaly detection.
**Steps:**
- Open a terminal and make sure the instructions in “Lab Setup” were applied.
- Create a virtual environment in python (Recommended)
- python -m venv path/to/venv
- source path/to/venv/bin/activate
- pip install -r requirements.txt
- Run preprocess.py to convert the provided .pcap file into csv and process it
- python scripts/preprocess.py
- Run analyze_anomalies.py to create anomalies csv and graph
- python scripts/analyze_anomalies.py
- Run live_packet_analysis.py to display real time anomaly detection graph
- python scripts/live_packet_analysis.py
- **Deliverable:** Run live_packet_analysis.py twice and post a screenshot for each of the graphs.

## Discussion:
- How do protocol-based filters (e.g., DNS, HTTP) help narrow down traffic for investigation?
- What additional features (e.g., source/destination IP patterns) would you consider adding for better anomaly detection?
- What are the advantages and limitations of automated anomaly detection compared to manual inspection?

## Additional Resources:
- https://github.com/FreeSoftWorks/PacketWorx
- https://www.geeksforgeeks.org/sniffing-of-login-credential-or-password-capturing-in-wireshark/
- https://youtu.be/qTaOZrDnMzQ?si=aj9jCm5-5ahVV1o_

