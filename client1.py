import tkinter as tk
from tkinter import ttk, messagebox
import socket
from cryptography.fernet import Fernet

class ClientApp:
    def __init__(self, master):
        self.master = master
        # Define a consistent font setting for labels, entries, and buttons
        label_font = ("", 18)
        entry_button_font = ("", 18)
        
        master.title("Encryption Client")
        master.geometry("400x300")  # Adjusted for potentially larger fonts

        # Apply font settings directly within widget creation
        ttk.Label(master, text="Text to encrypt:", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.text_entry = ttk.Entry(master, width=30, font=entry_button_font)
        self.text_entry.grid(row=0, column=1, padx=10, pady=5)

        self.encrypt_button = ttk.Button(master, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.grid(row=1, columnspan=2, padx=10, pady=5)

        ttk.Label(master, text="Received Key:", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        
        self.received_key = ttk.Entry(master, width=30, font=entry_button_font)
        self.received_key.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(master, text="Decrypt", command=self.decrypt_text).grid(row=3, columnspan=2, pady=5)

        ttk.Label(master, text="Decrypted Text:", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky='w')
        
        self.decrypted_text = ttk.Entry(master, width=30, state="readonly", font=entry_button_font)
        self.decrypted_text.grid(row=4, column=1, padx=10, pady=5)

    def encrypt_text(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', 6789))
                key = sock.recv(1024)  # Receive the encryption key from the server
                self.received_key.delete(0, tk.END)
                self.received_key.insert(0, key.decode('utf-8'))  # Ensure the key is properly decoded before displaying
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def decrypt_text(self):
        try:
            key = self.received_key.get().encode('utf-8')
            cipher_suite = Fernet(key)
            encrypted_message = cipher_suite.encrypt(self.text_entry.get().encode('utf-8'))
            decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
            self.decrypted_text.config(state=tk.NORMAL)
            self.decrypted_text.delete(0, tk.END)
            self.decrypted_text.insert(0, decrypted_message)
            self.decrypted_text.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
