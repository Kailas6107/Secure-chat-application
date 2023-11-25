import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import socket

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + '\n')
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)
        except OSError:  
            break

def send_message(event=None):  
    message = my_message.get()
    my_message.set("")  
    client_socket.send(bytes(message, "utf-8"))
    if message == "{quit}":
        client_socket.close()
        window.quit()

def on_closing(event=None):
    my_message.set("{quit}")
    send_message()

window = tk.Tk()
window.title("Chat Application")

messages_frame = tk.Frame(window)
my_message = tk.StringVar()  
my_message.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame) 

chat_box = scrolledtext.ScrolledText(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_box.pack(side=tk.LEFT, fill=tk.BOTH)
chat_box.config(state=tk.DISABLED)

messages_frame.pack()

entry_field = tk.Entry(window, textvariable=my_message)
entry_field.bind("<Return>", send_message)
entry_field.pack()
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

HOST = 'localhost'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = Thread(target=receive_messages)
receive_thread.start()

tk.mainloop()
