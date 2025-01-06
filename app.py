from flask import Flask, render_template, request, jsonify, send_file
from yt_dlp import YoutubeDL
import requests
import os

app = Flask(__name__)

# Configuración de reCAPTCHA
RECAPTCHA_SITE_KEY = "6Ld0aa0qAAAAAMQPew3iCQ0jXAjv8ieLf9F9-rlZ"
RECAPTCHA_SECRET_KEY = "6Ld0aa0qAAAAAJrbEnUxeFdJtxZHMrTnFMo88RKy"

# Ruta principal con reCAPTCHA
@app.route('/')
def index():
    return render_template('index.html', site_key=RECAPTCHA_SITE_KEY)

# Ruta para manejar descargas
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format')
    recaptcha_response = request.form.get('g-recaptcha-response')

    if not url or not recaptcha_response:
        return jsonify({"error": "URL o reCAPTCHA no válidos"}), 400

    # Verificar reCAPTCHA
    recaptcha_data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    recaptcha_verify = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_data).json()
    if not recaptcha_verify.get('success'):
        return jsonify({"error": "reCAPTCHA inválido"}), 400

    # Configuración de yt-dlp para descarga directa de formatos
    if format_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',  # Descargar el mejor formato de audio disponible
            'outtmpl': '%(title)s.mp3',  # Nombre del archivo
            'noplaylist': True,
            'cookiefile': 'cookies.txt',  # Ruta al archivo de cookies
        }
    else:  # Si es video, descargar en formato MP4
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',  # Aseguramos MP4 como formato de video
            'outtmpl': '%(title)s.mp4',  # Nombre del archivo
            'noplaylist': True,
            'cookiefile': 'cookies.txt',  # Ruta al archivo de cookies
        }

    try:
        # Descargar con yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            ydl.download([url])

        # Enviar archivo descargado
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"No se pudo descargar el archivo: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

