import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

threading.Thread(target=receive_messages, args=(client,)).start()

while True:
    message = input()
    client.send(message.encode())
