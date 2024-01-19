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

def get_target_directory():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Solicitar al usuario que seleccione la carpeta de destino
    target_directory = filedialog.askdirectory(title="Selecciona la carpeta a desencriptar")

    return target_directory

def get_key_location():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Solicitar al usuario que seleccione la ubicación de la clave
    key_location = filedialog.askopenfilename(title="Selecciona la clave de desencriptación", filetypes=[("Key files", "*.key")])

    return key_location

def decrypt_files_in_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)

# Obtener el directorio a desencriptar
target_directory = get_target_directory()

# Obtener la ubicación de la clave de desencriptación
key_location = get_key_location()

# Leer la clave desde el archivo seleccionado
with open(key_location, 'rb') as key_file:
    decryption_key = key_file.read()

# Desencriptar todos los archivos en el directorio seleccionado y sus subdirectorios
decrypt_files_in_directory(target_directory, decryption_key)

# Mostrar mensaje de éxito
messagebox.showinfo("Desencriptado", "Contenido de la carpeta desencriptado exitosamente.")
