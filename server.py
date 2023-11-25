import socket
import threading

def client_handler(connection):
    while True:
        try:
            message = connection.recv(1024).decode()
            print(message)
            broadcast(message, connection)
        except:
            break

def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen()

clients = []

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=client_handler, args=(conn,)).start()
