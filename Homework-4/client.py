import socket

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 8080)

    try:
        client_socket.connect(server_address)

        requests = [
            'GET / HTTP/1.1\r\n',
            'GET /about HTTP/1.1\r\n',
            'GET /product/0 HTTP/1.1\r\n',
            'GET /product/1 HTTP/1.1\r\n',
            'GET /nonexistent HTTP/1.1\r\n',
        ]

        for request in requests:
            client_socket.sendall(request.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(response)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()
