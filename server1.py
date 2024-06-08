import tkinter as tk
from tkinter import scrolledtext
import socket
from threading import Thread
from cryptography.fernet import Fernet

class ServerApp:
    def __init__(self, master):
        self.master = master
        master.title("Encryption Server")
        font_settings = ("", 12)
        self.log = scrolledtext.ScrolledText(master, state='disabled', width=100, height=30)
        self.log.grid(row=0, column=0, padx=10, pady=10)

        self.start_button = tk.Button(master, text="Start Server",font=font_settings, command=self.start_server)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

    def log_message(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + '\n')
        self.log.yview(tk.END)
        self.log.config(state='disabled')

    def handle_client_connection(self, client_socket):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        self.log_message(f"Generated encryption key: {key}")
        # Send the key to the client
        client_socket.send(key)
        self.log_message("Sent encryption key to client.")
        client_socket.close()

    def start_server_thread(self):
        HOST, PORT = 'localhost', 6789
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        self.log_message(f"Server listening on {HOST}:{PORT}")

        try:
            while True:
                client_sock, address = server_socket.accept()
                self.log_message(f"Accepted connection from {address}")
                self.handle_client_connection(client_sock)
        except Exception as e:
            self.log_message(f"Server error: {e}")
        finally:
            server_socket.close()

    def start_server(self):
        thread = Thread(target=self.start_server_thread, daemon=True)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
