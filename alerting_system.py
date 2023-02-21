import time
import socket

def ping(ip_address):
    """Sends a ping packet to the specified IP address."""
    socket1 = socket.socket()

    try:
        response = socket.gethostbyname(ip_address)
    except socket.gaierror:
        print("Error: Unknown host")
        return

    response = socket1.connect(ip_address, 79)
    if response is None:
        print("Error: Could not connect to host")
        return

    response.sendall("PING")
    response.recv(1024)
    response.close()

def periodic_server_check():
    """Pings a server IP address every 30 seconds until connection is failed."""
    ip_address = "192.168.1.1"
    while True:
        ping(ip_address)
        time.sleep(30)

def periodic_status_check():
    """Pings a server IP address every 30 seconds until connection is failed."""
    ip_address = "192.168.1.1"
    while True:
        ping(ip_address)
        time.sleep(30)