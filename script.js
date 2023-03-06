const form = document.getElementById('upload-form');
const imageInput = document.getElementById('image-input');
const resultContainer = document.getElementById('result-container');

form.addEventListener('submit', event => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            const image = new Image();
            image.src = `data:image/png;base64,${data.image}`;
            image.onload = () => {
                resultContainer.innerHTML = '';
                resultContainer.appendChild(image);
                resultContainer.style.display = 'block';
            }
        });
});
