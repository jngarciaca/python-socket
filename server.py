import socket 
  
def start_server(ip, port): 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    server_socket.bind((ip, port)) 

    server_socket.listen(5) 

    print(f"Servidor escuchando en {ip}:{port}") 

    return server_socket
  

if __name__ == "__main__": 

    server_socket = start_server("127.0.0.1", 5000) 
  
    connected_clients = []

    print("==== Log del servidor ====")
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida con {addr}") 
    data = client_socket.recv(1024).decode() 
    connected_clients.append(data)
    for client in connected_clients:
        username = client.encode()
        print(f"Usuario {username} is connected")
        client_socket.send(bytes(f"Usuario {username} is connected","UTF-8"))
    print(f"Usuarios conectados {len(connected_clients)}")
    while True: 
        if not data: break
        data = client_socket.recv(1024).decode()
        print(data)    
    client_socket.close()
    connected_clients.pop() 
