import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ConvertidorFFmpeg(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Convertidor HEIC/HEVC a JPEG/MP4")
        self.geometry("600x400")

        self.archivos = []

        self.btn_seleccionar = ctk.CTkButton(self, text="Seleccionar archivos HEIC/HEVC", command=self.seleccionar_archivos)
        self.btn_seleccionar.pack(pady=20)

        self.lista_archivos = ctk.CTkTextbox(self, height=10)
        self.lista_archivos.pack(fill="both", expand=True, padx=20, pady=(0,10))

        self.btn_convertir = ctk.CTkButton(self, text="Convertir", command=self.iniciar_conversion)
        self.btn_convertir.pack(pady=10)

        self.lbl_estado = ctk.CTkLabel(self, text="")
        self.lbl_estado.pack(pady=5)

    def seleccionar_archivos(self):
        archivos = filedialog.askopenfilenames(
            title="Selecciona archivos HEIC o HEVC",
            filetypes=[("HEIC y HEVC", "*.heic *.HEIC *.hevc *.HEVC")]
        )
        if archivos:
            self.archivos = list(archivos)
            self.lista_archivos.delete("0.0", "end")
            for f in self.archivos:
                self.lista_archivos.insert("end", f + "\n")
            self.lbl_estado.configure(text=f"{len(self.archivos)} archivo(s) seleccionados.")

    def iniciar_conversion(self):
        if not self.archivos:
            messagebox.showwarning("Atención", "No has seleccionado archivos para convertir.")
            return
        self.btn_convertir.configure(state="disabled")
        self.lbl_estado.configure(text="Convirtiendo...")
        threading.Thread(target=self.convertir_archivos, daemon=True).start()

    def convertir_archivos(self):
        errores = []
        for archivo in self.archivos:
            ext = os.path.splitext(archivo)[1].lower()
            if ext == ".heic":
                salida = os.path.splitext(archivo)[0] + ".jpeg"
                cmd = ["ffmpeg", "-y", "-i", archivo, salida]
            elif ext == ".hevc":
                salida = os.path.splitext(archivo)[0] + ".mp4"
                cmd = [
                    "ffmpeg", "-y", "-i", archivo,
                    "-c:v", "libx264",         # Video: compatible con Windows
                    "-profile:v", "main",     # Perfil compatible
                    "-pix_fmt", "yuv420p",     # Formato de color compatible
                    "-c:a", "aac",             # Audio en AAC
                    "-b:a", "192k",            # Bitrate razonable
                    "-movflags", "+faststart", # Mejora compatibilidad al comienzo
                    salida
                ]
            else:
                errores.append(f"Formato no soportado: {archivo}")
                continue

            try:
                resultado = subprocess.run(cmd, capture_output=True, text=True)
                if resultado.returncode != 0:
                    errores.append(f"Error al convertir {archivo}:\n{resultado.stderr}")
            except Exception as e:
                errores.append(f"Excepción al convertir {archivo}: {str(e)}")

        self.after(0, self.conversion_finalizada, errores)

    def conversion_finalizada(self, errores):
        self.btn_convertir.configure(state="normal")
        if errores:
            self.lbl_estado.configure(text="Conversión terminada con errores.")
            mensaje = "Algunos archivos no se convirtieron correctamente:\n\n" + "\n".join(errores)
            messagebox.showerror("Errores durante la conversión", mensaje)
        else:
            self.lbl_estado.configure(text="Conversión completada correctamente.")
            messagebox.showinfo("Éxito", "Todos los archivos se convirtieron correctamente.")

if __name__ == "__main__":
    app = ConvertidorFFmpeg()
    app.mainloop()
