import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def verificar_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except Exception:
        return False

class ConvertidorFFmpeg(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.carpeta_destino = ""

        if not verificar_ffmpeg():
            messagebox.showerror("FFmpeg no encontrado", "No se detectó FFmpeg en el sistema.\nAsegúrate de que esté instalado y agregado al PATH.")
            self.destroy()
            return

        self.title("Convertidor HEIC/HEVC/MOV a JPEG/MP4")
        self.geometry("600x450")

        self.archivos = []

        # Botón para seleccionar archivos
        self.btn_seleccionar = ctk.CTkButton(self, text="Seleccionar archivos HEIC/HEVC/MOV", command=self.seleccionar_archivos)
        self.btn_seleccionar.pack(pady=20)

        self.btn_carpeta = ctk.CTkButton(self, text="Seleccionar carpeta de destino", command=self.seleccionar_carpeta)
        self.btn_carpeta.pack(pady=5)

        # Label para mostrar carpeta destino
        self.lbl_carpeta = ctk.CTkLabel(self, text="Destino: carpeta original")
        self.lbl_carpeta.pack(pady=5)

        # Lista para mostrar archivos seleccionados
        self.lista_archivos = ctk.CTkTextbox(self, height=10)
        self.lista_archivos.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Barra de progreso
        self.progress = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progress.set(0)
        self.progress.pack(pady=10, padx=20, fill="x")

        # Botón convertir
        self.btn_convertir = ctk.CTkButton(self, text="Convertir", command=self.iniciar_conversion)
        self.btn_convertir.pack(pady=10)

        # Label para mostrar estado
        self.lbl_estado = ctk.CTkLabel(self, text="")
        self.lbl_estado.pack(pady=5)

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
        if carpeta:
            self.carpeta_destino = carpeta
            self.lbl_carpeta.configure(text=f"Destino: {carpeta}")
        else:
            self.carpeta_destino = ""
            self.lbl_carpeta.configure(text="Destino: carpeta original")

    def seleccionar_archivos(self):
        archivos = filedialog.askopenfilenames(
            title="Selecciona archivos HEIC, HEVC o MOV",
            filetypes=[("HEIC, HEVC y MOV", "*.mov *.MOV *.heic *.HEIC *.hevc *.HEVC")]
        )
        if archivos:
            self.archivos = list(archivos)
            self.lista_archivos.delete("0.0", "end")
            for f in self.archivos:
                self.lista_archivos.insert("end", f + "\n")
            self.lbl_estado.configure(text=f"{len(self.archivos)} archivo(s) seleccionados.")
            self.progress.set(0)

    def iniciar_conversion(self):
        if not self.archivos:
            messagebox.showwarning("Atención", "No has seleccionado archivos para convertir.")
            return
        self.btn_convertir.configure(state="disabled")
        self.lbl_estado.configure(text="Convirtiendo...")
        threading.Thread(target=self.convertir_archivos, daemon=True).start()

    def convertir_archivos(self):
        errores = []
        total = len(self.archivos)

        for i, archivo in enumerate(self.archivos, start=1):
            ext = os.path.splitext(archivo)[1].lower()
            nombre_base = os.path.splitext(os.path.basename(archivo))[0]

            if ext == ".heic":
                if self.carpeta_destino:
                    salida = os.path.join(self.carpeta_destino, nombre_base + ".jpeg")
                else:
                    salida = os.path.splitext(archivo)[0] + ".jpeg"
                cmd = ["ffmpeg", "-y", "-i", archivo, salida]

            elif ext == ".hevc":
                if self.carpeta_destino:
                    salida = os.path.join(self.carpeta_destino, nombre_base + ".mp4")
                else:
                    salida = os.path.splitext(archivo)[0] + ".mp4"
                cmd = [
                    "ffmpeg", "-y", "-i", archivo,
                    "-c:v", "libx264",
                    "-profile:v", "high",
                    "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709",
                    "-color_trc", "bt709",
                    "-colorspace", "bt709",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-movflags", "+faststart",
                    salida
                ]

            elif ext == ".mov":
                if self.carpeta_destino:
                    salida = os.path.join(self.carpeta_destino, nombre_base + ".mp4")
                else:
                    salida = os.path.splitext(archivo)[0] + ".mp4"
                cmd = ["ffmpeg", "-y", "-i", archivo, "-c:v", "libx264", "-c:a", "aac", salida]

            else:
                errores.append(f"Formato no soportado: {archivo}")
                continue

            try:
                resultado = subprocess.run(cmd, capture_output=True, text=True)
                if resultado.returncode != 0:
                    errores.append(f"Error al convertir {archivo}:\n{resultado.stderr}")
            except Exception as e:
                errores.append(f"Excepción al convertir {archivo}: {str(e)}")

            progreso = i / total
            self.progress.set(progreso)

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
        self.progress.set(0)


if __name__ == "__main__":
    app = ConvertidorFFmpeg()
    app.mainloop()
