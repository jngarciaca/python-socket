import socket 
import json
import threading

client_id = None

def start_client(ip, port, username): 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    client_socket.connect((ip, port)) 

    client_socket.send(username.encode()) 

    response = client_socket.recv(1024).decode() 
    client_id = response

    print(f"Tu Id de cliente es: {client_id}")
    connected_clients = client_socket.recv(1024).decode()
    print("Usuarios connectados:")
    print(connected_clients)

    return client_socket, client_id

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            decoded_message = json.loads(message)
            print("\n{}: {}".format(decoded_message.get("username"),decoded_message.get("msg")))
        except ConnectionResetError:
            break

if __name__ == "__main__": 

    server_ip = input("IP del servidor: ")
    port = int(input("Port: "))
    username = input("Escriba su nombre: ")
    try:
        client_socket, client_id = start_client(server_ip, port, username)

        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
        receive_thread.start()
        target_id = input("Elija un ID de usuario para chatear: ")    
        while True:
            message = input(">> ")
            message_dict = {"id": client_id, "username": username, "target_id": target_id, "msg": message}
            data = json.dumps(message_dict)
            client_socket.sendall(data.encode())
    except socket.error as e:
        print(str(e))
    finally:
        client_socket.close()
    