document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('convert-form');
    const urlInput = document.getElementById('youtube-url');
    const formatSelect = document.getElementById('format-select');
    const videoPreview = document.getElementById('video-preview');

    // Función para extraer el ID del video de YouTube
    function extractVideoID(url) {
        const regex = /(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
        const match = url.match(regex);
        return match ? match[1] : null;
    }

    // Función para mostrar la previsualización del video
    function showVideoPreview(videoId) {
        if (!videoId) return;

        const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
        const videoInfo = videoPreview.querySelector('.video-info');
        const thumbnail = videoPreview.querySelector('.video-thumbnail');
        
        // Actualizar la imagen de previsualización
        thumbnail.src = thumbnailUrl;
        thumbnail.alt = 'Video thumbnail';

        // Mostrar el contenedor de previsualización
        videoPreview.style.display = 'block';

        // Obtener el título del video usando la API de oEmbed de YouTube
        fetch(`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`)
            .then(response => response.json())
            .then(data => {
                videoPreview.querySelector('.video-title').textContent = data.title;
                videoPreview.querySelector('.video-duration').textContent = 'YouTube Video';
            })
            .catch(error => {
                console.error('Error fetching video details:', error);
                videoPreview.querySelector('.video-title').textContent = 'Video de YouTube';
                videoPreview.querySelector('.video-duration').textContent = '';
            });
    }

    // Evento para mostrar la previsualización cuando se pega una URL
    urlInput.addEventListener('input', function() {
        const videoId = extractVideoID(this.value);
        if (videoId) {
            showVideoPreview(videoId);
        } else {
            videoPreview.style.display = 'none';
        }
    });

    // Manejar el envío del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Verificar el reCAPTCHA
        const recaptchaResponse = grecaptcha.getResponse();
        if (!recaptchaResponse) {
            alert('Por favor, completa el captcha');
            return;
        }

        const url = urlInput.value;
        const format = formatSelect.value;
        
        // Aquí iría la lógica de conversión
        console.log(`Convirtiendo ${url} a ${format}`);
        alert(`Iniciando conversión de ${url} a formato ${format}`);
        
        // Reiniciar el formulario y el captcha
        form.reset();
        grecaptcha.reset();
        videoPreview.style.display = 'none';
    });
});