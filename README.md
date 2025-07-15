# HEIC-HEVC-converter
An HEIC/HEVC to .JPEG and .MOV converter


install requeriments: 

pip install customtkinter pillow pyheif

Necesitas tener instalado ffmpeg y que esté en la variable PATH del sistema para poder llamarlo desde Python con subprocess.


        Pasos para instalar ffmpeg en Windows:

            Descarga el build precompilado:

            Ve a la web oficial: https://ffmpeg.org/download.html

            En la sección de Windows, suele recomendarte builds de terceros como https://www.gyan.dev/ffmpeg/builds/

            Descarga la versión release full (por ejemplo, ffmpeg-release-full.zip).

            Descomprime el ZIP en una carpeta, por ejemplo:
            C:\ffmpeg

            Agrega ffmpeg al PATH del sistema:

            Abre el Panel de Control → Sistema → Configuración avanzada del sistema → Variables de entorno.

            En "Variables del sistema", busca la variable Path y haz clic en "Editar".

            Añade una nueva entrada con la ruta completa al subdirectorio bin de ffmpeg, por ejemplo:
            C:\ffmpeg\bin

            Guarda y cierra.

            Verifica que ffmpeg esté instalado:

            Abre la consola CMD o PowerShell.

            Escribe:

            bash
            Copiar
            Editar
            ffmpeg -version
            Si te muestra información de la versión, está listo para usar.

