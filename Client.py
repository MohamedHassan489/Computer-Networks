import socket

def client_program(server_ip='127.0.0.1', server_port=5353):
    """Client program to query DNS server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    try:
        print("Query format: '<TYPE> <DOMAIN>' (e.g., 'A example.com' or 'PTR 93.184.216.34')")
        query = input("Enter your query: ").strip()

        # Send query to the server
        client.send(query.encode('utf-8'))

        # Receive and print response
        response = client.recv(1024).decode('utf-8')
        print(response)
    finally:
        client.close()

if __name__ == "__main__":
    client_program()
