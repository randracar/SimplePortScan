import socket
import threading
from concurrent.futures import ThreadPoolExecutor

openports = []
lock = threading.Lock()

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)  # Adjust the timeout as needed

            try:
                sock.connect((target, port))
                with lock:
                    print(f"Port {port} is open")
                    openports.append(port)
            except socket.error:
                pass  
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def main():
    try:
        target = input("Enter the target IP address or hostname: ")
        min_port = int(input("Enter the starting port: "))
        max_port = int(input("Enter the ending port: "))

        print(f"Scanning ports {min_port} to {max_port} on {target}...\n")

        max_workers = min(100, max_port - min_port + 1)  
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for port in range(min_port, max_port + 1):
                executor.submit(scan_port, target, port)

        print("\nScan ended\n")

        if openports:
            print("Open ports:")
            for port in openports:
                print(f"Port {port} is open")
        else:
            print("No open ports found.")
    except KeyboardInterrupt:
        print("\nScan was interrupted by the user.")

if __name__ == "__main__":
    main()
