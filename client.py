import socket 
import json

client_id = None

def start_client(ip, port, username): 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    client_socket.connect((ip, port)) 

    client_socket.send(username.encode()) 

    response = client_socket.recv(1024).decode() 
    client_id = response

    print(f"Tu Id de cliente es: {client_id}")

    return client_socket, client_id

  

if __name__ == "__main__": 

    server_ip = input("IP del servidor: ")
    port = int(input("Port: "))
    username = input("Escriba su nombre: ")
    try:
        client_socket, client_id = start_client(server_ip, port, username)
        while True:
            message = input(">> ")
            message_dict = {"id": client_id, "msg": message}
            data = json.dumps(message_dict)
            client_socket.sendall(data.encode())
    except socket.error as e:
        print(str(e))
    finally:
        client_socket.close()
    