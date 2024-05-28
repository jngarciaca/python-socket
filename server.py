import socket
import json 
import threading
  
def start_server(ip, port): 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    server_socket.bind((ip, port)) 

    server_socket.listen(5) 

    print(f"Servidor escuchando en {ip}:{port}") 

    return server_socket

def broadcast_message(message,sender_socket):
    for client in connected_clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error al enviar mensaje a {client}: {e}")
                client.close()
                connected_clients.remove(client)

def send_message_to_target(message, target_id):
    target_socket = None
    for client in connected_clients:
        if target_id == client.getpeername()[1]:
            target_socket = client
    if target_socket:
        try:
            target_socket.send(message)
        except Exception as e:
            print(f"Error al enviar mensaje a {client}: {e}")
            target_socket.close()
            connected_clients.remove(target_socket)

def handle_clients(client_socket, addr, connected_clients):
    client_id = addr[1]
    print(f"Conexión establecida con {addr}") 
    client_socket.send(bytes(f"{client_id}","UTF-8"))
    for client in connected_clients:
        client_socket.send(bytes(f"{client.getpeername()[1]}\n","UTF-8"))
    username = client_socket.recv(1024).decode() 
    print(f"Usuario: {username} esta conectado")
    while True:
        try:
            data = client_socket.recv(1024).decode()
            message = json.loads(data)
            if message["msg"] == "chao": break
            if not data: break
            print(f"Usuarios conectados {len(connected_clients)}")
            #broadcast_message(data.encode(), client_socket)
            send_message_to_target(data.encode(), int(message["target_id"]))
            print(message)    
        except ConnectionResetError:
            break
    client_socket.close()
    connected_clients.remove(client_socket) 
    print(f"Usuario: {username} ha abandonado")

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