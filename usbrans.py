import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    f = Fernet(key)
    encrypted_data = f.encrypt(data)

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

def generate_key(key_path):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)

def get_target_directory():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Solicitar al usuario que seleccione la carpeta de destino
    target_directory = filedialog.askdirectory(title="Selecciona la carpeta a encriptar")

    return target_directory

def get_key_save_location():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Solicitar al usuario que seleccione dónde guardar la clave
    key_save_location = filedialog.asksaveasfilename(title="Selecciona dónde guardar la clave", defaultextension=".key", filetypes=[("Key files", "*.key")])

    return key_save_location

def encrypt_files_in_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)

# Obtener el directorio a encriptar
target_directory = get_target_directory()

# Obtener la ubicación donde guardar la clave
key_save_location = get_key_save_location()

# Generar una clave de cifrado única y guardarla en la ubicación seleccionada
generate_key(key_save_location)

# Leer la clave desde el archivo recién creado
with open(key_save_location, 'rb') as key_file:
    encryption_key = key_file.read()

# Encriptar los archivos en el directorio seleccionado
encrypt_files_in_directory(target_directory, encryption_key)

# Mostrar mensaje de éxito
messagebox.showinfo("Encriptado", "Archivos encriptados exitosamente.")
