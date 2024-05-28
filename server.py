import socket
import json 
import threading
  
def start_server(ip, port): 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    server_socket.bind((ip, port)) 

    server_socket.listen(5) 

    print(f"Servidor escuchando en {ip}:{port}") 

    return server_socket

def handle_clients(client_socket, addr, connected_clients):
    client_id = addr[1]
    print(f"Conexión establecida con {addr}") 
    client_socket.send(bytes(f"{client_id}","UTF-8"))
    data = client_socket.recv(1024).decode() 
    print(f"Usuario: {data} esta conectado")
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if json.loads(data)["msg"] == "chao": break
            if not data: break
            print(f"Usuarios conectados {len(connected_clients)}")
            print(json.loads(data)["msg"])    
        except ConnectionResetError:
            break
    client_socket.close()
    connected_clients.remove(client_socket) 
    print(f"Conexion con {addr} cerrada")

if __name__ == "__main__": 

    server_socket = start_server("127.0.0.1", 5000) 
  
    connected_clients = []

    try:
        while True: 
            client_socket, addr = server_socket.accept()
            connected_clients.append(client_socket)
            client_thread = threading.Thread(target=handle_clients, args=(client_socket, addr, connected_clients))
            client_thread.start()
            print("==== Log del servidor ====")
    except KeyboardInterrupt:
        print("Servidor detenido")
    finally:
        for client in connected_clients:
            client.close()
        server_socket.close()