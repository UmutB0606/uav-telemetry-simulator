# Secure UAV Telemetry Simulator & GCS Dashboard

A robust, real-time Unmanned Aerial Vehicle (UAV) telemetry simulator and Ground Control Station (GCS) dashboard. Built with Python, this project demonstrates core defense industry software concepts including low-latency UDP networking, End-to-End Encryption (COMSEC), and multi-threaded real-time data visualization.

## 🚀 Core Architecture & Features

- **Encrypted UDP Data Link (COMSEC):** Telemetry data is completely encrypted using AES-128 (Fernet) before being transmitted over the network. This prevents Man-in-the-Middle (MitM) attacks and unauthorized packet sniffing.
- **Low-Latency UDP Networking:** Utilizes "Fire and Forget" UDP sockets instead of TCP to ensure real-time data delivery without lag caused by packet retransmission—a critical requirement for C2 (Command & Control) systems.
- **Multi-Threaded GCS Receiver:** The Ground Control Station uses Daemon Threads to separate the network listening socket from the main UI thread. This eliminates bottlenecks and ensures the UI never freezes while receiving heavy data streams.
- **Flight Physics Simulation:** The UAV simulator generates realistic, boundary-checked flight metrics (Altitude, Speed, Pitch, Roll, Yaw) avoiding erratic or physically impossible data spikes.
- **Real-Time UI Dashboard:** Built with Matplotlib, rendering high-performance live scrolling plots for UAV altitude and speed.

## 🛠️ Technology Stack
- **Language:** Python 3.x
- **Networking:** `socket` (IPv4, UDP/Datagram)
- **Encryption:** `cryptography` (AES-128 Fernet)
- **Concurrency:** `threading`
- **Visualization:** `matplotlib`

## ⚙️ How to Run the System

1. **Install Dependencies:**
   ```bash
   pip install matplotlib cryptography

Start the Ground Control Station (Receiver):
   Open a terminal and run the GCS to start listening on the secure UDP port:
   python gcs_receiver.py

Launch the UAV (Transmitter):
    Open a second terminal and run the simulator to start generating and broadcasting encrypted telemetry:
    python uav_simulator.py