#!/usr/bin/env python3

import socket

def start_chat_server():
    host = 'localhost'
    port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"\n [+] Servidor listo para aceptar una conexión...")
    connection, client_addr = server_socket.accept()
    print(f"\n [+] Se ha conectado el cliente {client_addr}")

    while True:
        client_message = connection.recv(1024).strip().decode()
        print(f"\n[+] Mensaje del cliente: {client_message}")
        
        if client_message == 'bye':
            break
        
        server_message = input(f"\n[+] Mensaje para enviar al cliente: ")
        connection.send(server_message.encode())

    connection.close()


start_chat_server()
