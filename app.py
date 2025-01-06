from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
from io import BytesIO

app = Flask(__name__)

# Ruta al archivo de cookies exportado desde el navegador
COOKIE_FILE = "cookies.txt"

def apply_cookies_to_pytube(url):
    """
    Inicializa la instancia de YouTube con cookies cargadas desde un archivo.
    """
    # Crear una instancia de YouTube con el archivo de cookies
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=True, use_po_token=True)
    return yt

def download_video_or_audio(url, format_type):
    """
    Descarga un video o audio de YouTube y lo guarda en memoria.
    """
    yt = apply_cookies_to_pytube(url)

    # Seleccionar el stream basado en el formato
    if format_type == 'audio':
        stream = yt.streams.filter(only_audio=True).first()
    else:
        stream = yt.streams.get_highest_resolution()

    # Descargar el archivo al buffer
    buffer = BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)

    title = yt.title
    ext = 'mp3' if format_type == 'audio' else 'mp4'
    return buffer, title, ext

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Obtener la URL del video desde el formulario
        url = request.form.get('video_url')
        format_type = request.form.get('format')  # Obtener el formato seleccionado

        # Descargar el video o audio
        buffer, title, ext = download_video_or_audio(url, format_type)

        # Descargar el archivo a través del navegador
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{title}.{ext}",
            mimetype="audio/mpeg" if ext == 'mp3' else "video/mp4"
        )

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)


