import subprocess #Para procesos en 2 plano sobre todo PS
import time #Para el time.sleep
import tkinter as tk #Interfaz grafica bonita
from tkinter import ttk, messagebox #Más interfaz grafica
from threading import Thread #Hilos para la rapidez del programa
import os
import tempfile #Para hacer archivos temporales de los logs

def ejecutar_comando_powershell(comando):
    resultado = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)
    return resultado.stdout.strip()

def verificar_modulo_pswindowsupdate():
    comando = "Get-Module -ListAvailable -Name PSWindowsUpdate"
    resultado = ejecutar_comando_powershell(comando)
    if not resultado:
        instalar_modulo_pswindowsupdate()
    else:
        print("PSWindowsUpdate ya está instalado.")

def instalar_modulo_pswindowsupdate():
    comando = "Install-Module -Name PSWindowsUpdate -Force -Confirm:$false"
    resultado = ejecutar_comando_powershell(comando)
    print("Resultado de la instalación del módulo:\n", resultado)

def buscar_actualizaciones():
    comando = "Get-WindowsUpdate"
    resultado = ejecutar_comando_powershell(comando)
    print("Actualizaciones disponibles:\n", resultado)

def instalar_actualizaciones():
    comando = "Install-WindowsUpdate -AcceptAll -AutoReboot"
    resultado = ejecutar_comando_powershell(comando)
    print("Resultado de la instalación de actualizaciones:\n", resultado)

def run_commands(progress_bar, status_label, root):
    def update_progress(value):
        progress_bar["value"] = value

    status_label.config(text="Repairing Disk...")

    try:
        temp_dir = tempfile.gettempdir()
        
        # Reparando el disco
        update_progress(0)
        chkdsk_output_file = os.path.join(temp_dir, "chkdsk_result.txt")
        with open(chkdsk_output_file, "w") as f:
            subprocess.run(["chkdsk"], shell=True, stdout=f, stderr=subprocess.STDOUT)
        time.sleep(1)

        # Escaneando
        update_progress(20)
        sfc_output_file = os.path.join(temp_dir, "sfc_result.txt")
        with open(sfc_output_file, "w") as f:
            subprocess.run(["sfc", "/scannow"], shell=True, stdout=f, stderr=subprocess.STDOUT)
        time.sleep(1)

        # Comprobando la salud del disco
        update_progress(45)
        dism_scan_output_file = os.path.join(temp_dir, "dism_scan_result.txt")
        with open(dism_scan_output_file, "w") as f:
            subprocess.run(["DISM.exe", "/Online", "/Cleanup-Image", "/ScanHealth"], shell=True, stdout=f, stderr=subprocess.STDOUT)
        time.sleep(1)

        # Restaurando el disco
        update_progress(60)
        dism_restore_output_file = os.path.join(temp_dir, "dism_restore_result.txt")
        with open(dism_restore_output_file, "w") as f:
            subprocess.run(["DISM.exe", "/Online", "/Cleanup-Image", "/RestoreHealth"], shell=True, stdout=f, stderr=subprocess.STDOUT)
        time.sleep(1)

        # Comprobando la limpieza
        update_progress(80)
        dism_check_output_file = os.path.join(temp_dir, "dism_check_result.txt")
        with open(dism_check_output_file, "w") as f:
            subprocess.run(["DISM.exe", "/Online", "/Cleanup-Image", "/CheckHealth"], shell=True, stdout=f, stderr=subprocess.STDOUT)
        time.sleep(1)
        status_label.config(text="Disk Repaired")

        # Progress for Updates
        update_progress(90)
        update_and_reboot(root)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error during disk repair: {str(e)}")

def update_and_reboot(root):
    # Mostrar un mensaje de advertencia antes de la actualización
    proceed = messagebox.askyesno("Update System", "The disk has been repaired. Do you want to update your system now?")
    
    if proceed:
        update_choice = messagebox.askyesnocancel("Choose Updates", "Do you want to update Windows too? No for only Drivers, Cancel for none.")
        try:
            if update_choice is None:  # Cancel
                # Cerrar la ventana principal si el usuario cancela la actualización
                root.destroy()
            elif update_choice:  # Yes -> Update both
                # Actualizar Windows
                verificar_modulo_pswindowsupdate()
                buscar_actualizaciones()
                instalar_actualizaciones()
                messagebox.showinfo("All Windows Update installed")
                # Actualizar Lenovo
                run_lenovo_update(root)
            else:  # No -> Only Lenovo
                # Actualizar Lenovo
                run_lenovo_update(root)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start system update: {str(e)}")
    else:
        # Cerrar la ventana principal si el usuario cancela la actualización
        root.destroy()

def run_lenovo_update(root):
    try:
        # Variables para Lenovo Commercial Vantage
        appid = "E046963F.LenovoSettingsforEnterprise_k1h2ywk1493x8!App"
        command = f'shell:appsfolder\\{appid}'

        # Comando a trozos
        subprocess.run([
            "powershell",
            "-Command",
            f'Start-Process "{command}" -ArgumentList "lenovo-vantage3:system-updates?action=start"'
        ], shell=True)

        # Cerrar la ventana principal despues de llamar a lenovo
        root.destroy()
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start Lenovo update: {str(e)}")

def reparar_disco():
    root = tk.Tk()
    root.title("Progress")

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    status_label = tk.Label(root, text="Repairing Disk...")
    status_label.pack()

    # Deshabilitar cierre de ventana
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Ejecutar los comandos en un hilo separado
    command_thread = Thread(target=run_commands, args=(progress_bar, status_label, root))
    command_thread.start()

    root.mainloop()

if __name__ == "__main__":
    reparar_disco()
