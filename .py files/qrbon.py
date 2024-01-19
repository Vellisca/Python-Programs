import tkinter as tk
from tkinter import messagebox
import qrcode

def generar_qr():
    # Obtener el texto ingresado por el usuario
    data = entry.get()
    
    # Crear un objeto QRCode
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    
    # Agregar los datos al código QR
    qr.add_data(data)
    qr.make(fit=True)
    
    # Crear una imagen del código QR
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("codigo_qr.png")
    
    messagebox.showinfo("Generador de Códigos QR", "Código QR generado exitosamente.")

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Códigos QR")

# Definir el tamaño de la ventana
root.geometry("760x400")

# Minimizar la ventana al inicio
root.iconify()

# Crear un marco para organizar los widgets
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Etiqueta
label = tk.Label(frame, text="Ingrese el texto:")
label.pack(padx=5, pady=5)

# Campo de entrada
entry = tk.Entry(frame, width=70)
entry.pack(padx=5, pady=5)

# Botón
btn_generar = tk.Button(frame, text="Generar Código QR", command=generar_qr)
btn_generar.pack(padx=5, pady=10)

# Establecer el color de fondo del marco
frame.configure(bg="#f0f0f0")  # Cambiar el color de fondo a gris claro

# Cambiar el estilo del botón
btn_generar.configure(bg="#4caf50", fg="white", relief="raised")  # Cambiar colores y relieve

# Mostrar la ventana
root.deiconify()

# Iniciar el bucle principal
root.mainloop()
