import socket
import threading

# Server configuration
hostname = socket.gethostname()
server_ip = socket.gethostbyname(hostname)
print(server_ip)
server_port = 12345

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # Handle client request and send a response
            response = process_client_request(message)

            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            break

    # Remove the client from the list
    clients.remove(client_socket)
    client_socket.close()

def process_client_request(request):
    # Replace this with your logic to process client requests and generate responses
    # For this example, we'll simply return the received request.
    return "Server Response: " + request

print("Server is listening on {}:{}".format(server_ip, server_port))

while True:
    client_socket, client_addr = server_socket.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()