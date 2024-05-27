import socket
import random 
import json

def start_client(ip, port, username): 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    client_socket.connect((ip, port)) 

    client_socket.send(username.encode()) 

    response = client_socket.recv(1024).decode() 

    print(f"Respuesta del servidor: {response}")

    #client_socket.close()

    return client_socket

  

if __name__ == "__main__": 

    server_ip = input("IP del servidor: ")
    port = int(input("Port: "))
    username = input("Escriba su nombre: ")
    client_id = random.randrange(9999)
    try:
        while True:
            client_socket = start_client(server_ip, port, username)
            message = input(">> ")
            message_dict = {"id": client_id, "msg": message}
            data = json.dumps(message_dict)
            client_socket.sendall(data.encode())
            client_socket.close()
    except socket.error as e:
        print(str(e))
    #finally:
        #client_socket.close()
    