import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

def receive_messages(client_socket, chat_box):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + '\n')
            chat_box.config(state=tk.DISABLED)
        except ConnectionAbortedError:
            break

def send_message(message_entry, client_socket, chat_box):
    message = message_entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, "You: " + message + '\n')
        chat_box.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)

def on_closing(root, client_socket):
    print("closing...")
    client_socket.close()
    root.destroy()

def get_chat_window():
    root = tk.Tk()
    root.title("Live Chat")
    root.geometry("300x600+600+100")

    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
    chat_box.pack(fill=tk.BOTH, expand=True)

    message_entry = tk.Entry(root, width=50)
    message_entry.pack(pady=5)

    server_ip = "192.168.1.108"
    server_port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    receive_thread = threading.Thread(target=lambda: receive_messages(client_socket, chat_box))
    receive_thread.daemon = True
    receive_thread.start()

    send_button = tk.Button(root, text="Send", command=lambda: send_message(message_entry, client_socket, chat_box))
    send_button.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, client_socket))
    root.mainloop()

# Example of triggering the chat window
if __name__ == "__main__":
    root = tk.Tk()
    chat_button = tk.Button(root, text="Open Chat", command=get_chat_window)
    chat_button.pack()
    root.mainloop()
