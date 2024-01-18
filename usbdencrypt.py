import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)

    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

def get_decryption_key():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Solicitar al usuario que seleccione el archivo de clave
    key_file_path = filedialog.askopenfilename(title="Selecciona el archivo de clave", filetypes=[("Key files", "*.key")])

    # Leer la clave desde el archivo seleccionado
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

    return key

def get_target_directory():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Solicitar al usuario que seleccione el directorio de destino
    target_directory = filedialog.askdirectory(title="Selecciona el directorio de destino")

    return target_directory

def decrypt_files_in_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)

# Obtener la clave de desencriptado
decryption_key = get_decryption_key()

# Obtener el directorio de destino
target_directory = get_target_directory()

# Desencriptar los archivos en el directorio de destino seleccionado
decrypt_files_in_directory(target_directory, decryption_key)

# Mostrar mensaje de éxito
messagebox.showinfo("Desencriptado", "Archivos desencriptados exitosamente.")
