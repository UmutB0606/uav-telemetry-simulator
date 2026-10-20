import socket
import json
import threading
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

raw_key = os.getenv("ASELSAN_SECRET_KEY")
if not raw_key:
    raise ValueError("ERROR: key not found")

SECRET_KEY = raw_key.encode('utf-8')
cipher_suite = Fernet(SECRET_KEY)

# Telemetry Data Queues
# We hold last 50 data with deque, thus graphic will slide to right lively.
altitude_data = deque(maxlen=50)
speed_data = deque(maxlen=50)

def udp_listener():
    """Background thread function to listen for UDP packets continuously."""
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"--- GCS Network Listener [SECURE MODE] Active ---")

    while True:
        try:
            # Receive and decode data
            encrypted_data, _ = sock.recvfrom(2048)

            decrypted_data = cipher_suite.decrypt(encrypted_data)
            
            # Add incoming data to the right end of the queues
            telemetry = json.loads(decrypted_data.decode('utf-8'))
            altitude_data.append(telemetry['altitude'])
            speed_data.append(telemetry['speed'])
        except Exception as e:
            print(f"Decryption/Network Error: {e}")

def update_graph(frame):
    """Main thread function to update the Matplotlib plots."""
    ax1.clear()
    ax2.clear()

    if len(altitude_data) > 0:
        # Plot Altitude
        ax1.plot(altitude_data, color='dodgerblue', linewidth=2, label='Altutide (m)')
        ax1.set_title('UAV Real-Time Altitude')
        ax1.set_ylabel('Meters')
        ax1.legend('upper left')
        ax1.grid(True, linestyle="--", alpha=0.7)

        # Plot Speed
        ax2.plot(speed_data, color='crimson', linewidth=2, label='Speed (km/h)')
        ax2.set_title('UAV Real-Time Speed')
        ax2.set_ylabel('km/h')
        ax2.legend(loc='upper left')
        ax2.grid(True, linestyle='--', alpha=0.7)

if __name__ == "__main__":
    # 1. Start the Network Listener in a separate Daemon Thread
    # Daemon thread means it will automatically close when we close the graph window
    listener_thread = threading.Thread(target=udp_listener, daemon=True)
    listener_thread.start()

    # 2. Setup the GUI / Dashboard Figure
    print("--- Launching GCS Dashboard ---")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6))
    fig.tight_layout(pad=4.0)
    fig.canvas.manager.set_window_title('Aselsan UAV GCS Prototype')

    # 3. Animate the graph, updating every 1000 milliseconds (1 second)
    ani = animation.FuncAnimation(fig, update_graph, interval=1000)
    
    # 4. Display the window (This blocks the main thread, which is why we needed the background thread!)
    plt.show()

    ani = animation.FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)