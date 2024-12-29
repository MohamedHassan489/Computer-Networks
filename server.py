import socket
import threading
import time

# DNS records
DNS_DATABASE = {
    "example.com": {"A": "93.184.216.34", "CNAME": "alias.example.com"},
    "google.com": {"A": "142.250.190.14"},
    "localhost": {"A": "127.0.0.1"},
    "93.184.216.34": {"PTR": "example.com"}
}

# TTL for caching (in seconds)
TTL_DATABASE = {
    "example.com": 300,
    "google.com": 300,
    "localhost": 300,
    "93.184.216.34": 300
}

# Error codes
ERROR_CODES = {
    "NOERROR": "Query completed successfully.",
    "NXDOMAIN": "Domain name does not exist.",
    "SERVFAIL": "Server failed to complete the query."
}

def format_dns_response(query, qtype):
    """Generate a DNS response based on the query and type."""
    domain = query.lower()  # Case-insensitive as per RFC 2181
    if domain in DNS_DATABASE:
        if qtype in DNS_DATABASE[domain]:
            # Include TTL in the response
            return f"Response: {qtype} record for {domain} is {DNS_DATABASE[domain][qtype]} | TTL: {TTL_DATABASE[domain]} | {ERROR_CODES['NOERROR']}"
        else:
            return f"{qtype} record not found for {domain} | {ERROR_CODES['NXDOMAIN']}"
    else:
        return f"{domain} | {ERROR_CODES['NXDOMAIN']}"

def handle_client(client_socket, client_address):
    """Handle DNS query from a client."""
    print(f"[INFO] Connected to {client_address}")
    try:
        # Receive query
        query = client_socket.recv(1024).decode('utf-8').strip()
        query_parts = query.split(" ")
        if len(query_parts) == 2:
            qtype = query_parts[0]
            domain = query_parts[1]
            response = format_dns_response(domain, qtype)
        else:
            response = f"Invalid query format. Expected '<TYPE> <DOMAIN>'. | {ERROR_CODES['SERVFAIL']}"

        # Send response
        client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] {e}")
        client_socket.send(f"Error processing query. | {ERROR_CODES['SERVFAIL']}".encode('utf-8'))
    finally:
        client_socket.close()
        print(f"[INFO] Disconnected from {client_address}")

def server_status():
    """Print server status periodically."""
    while True:
        print("[STATUS] DNS Server is running...")
        time.sleep(10)

def start_server(host='0.0.0.0', port=5353):
    """Start the DNS server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # Allow up to 5 simultaneous connections
    print(f"[STARTED] DNS Server is running on {host}:{port}")

    threading.Thread(target=server_status, daemon=True).start()

    try:
        while True:
            client_socket, client_address = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        print("[SHUTDOWN] DNS Server is shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()

