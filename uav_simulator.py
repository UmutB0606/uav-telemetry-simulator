import time
import random
import json
import socket
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

raw_key = os.getenv("ASELSAN_SECRET_KEY")
if not raw_key:
    raise ValueError("ERROR: key not found")

SECRET_KEY = raw_key.encode('utf-8')
cipher_suite = Fernet(SECRET_KEY)

class UAVSimulator:
    def __init__(self):
        # Initial starting values for the drone
        self.altitude = 150.0 # meters
        self.speed = 60.0 # km/h
        self.pitch = 0.0 # degrees (Nose up/down)
        self.roll = 0.0 # degrees (Tilting left/right)
        self.yaw = 90.0 # degrees (Heading direction)

    def update_telemetry(self):
        # Adding smooth random noise to simulate real flight physics
        self.altitude += random.uniform(-1.5, 1.5)
        self.speed += random.uniform(-2.0, 2.0)
        self.pitch += random.uniform(-0.5, 0.5)
        self.roll += random.uniform(-1.0, 1.0)
        self.yaw += random.uniform(-1.0, 1.0)

        # Keep values within realistic physical bounds
        self.altitude = max(0.0, self.altitude)
        self.speed = max(0.0, self.speed)
        self.yaw = self.yaw % 360
    def get_data(self):
        # Package the data into a JSON structure
        # We will use this JSON format to send data over the network later
        return {
            "timestamp": time.time(),
            "altitude": round(self.altitude, 2),
            "speed": round(self.speed, 2),
            "pitch": round(self.pitch, 2),
            "roll": round(self.roll, 2),
            "yaw": round(self.yaw, 2)
        }
if __name__ == "__main__":
    drone = UAVSimulator()

    # UDP Socket Configuration
    TARGET_IP = "127.0.0.1" # Localhost
    UDP_PORT = 5005

    # Create UDP Socket (IPv4, Datagram)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"--- UAV Telemetry Transmitter [ENCRYPTED] Started ---")

    try:
        while True:
            drone.update_telemetry()
            telemetry_data = drone.get_data()

            # Pack data into JSON and encode to bytes for network transfer
            raw_payload = json.dumps(telemetry_data).encode('utf-8')

            encrypted_payload = cipher_suite.encrypt(raw_payload)

            # Send packet over the network
            sock.sendto(encrypted_payload, (TARGET_IP, UDP_PORT))

            print(f"Sent Encrypted Packet: {encrypted_payload[:40]}...")

            # Send data every 1 second (1 Hz frequency)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--- Transmitter Stopped ---")