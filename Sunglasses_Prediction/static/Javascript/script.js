const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const constraints = { video: true };

let stream; // Store the stream to be able to stop it later

navigator.mediaDevices.getUserMedia(constraints)
    .then(mediaStream => {
        stream = mediaStream; // Store the stream
        video.srcObject = mediaStream;
    })
    .catch(error => {
        console.error('Error accessing camera:', error);
    });

captureButton.addEventListener('click', () => {
    // Pause or stop the video stream before capturing the image
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.style.display = 'none'; // Hide the video element
    }

    // Capture the current frame of the video and draw it on the canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    const image = canvas.toDataURL('image/png');
    sendImageToBackend(image);

    // Show the captured image on the canvas
    captureButton.style.display = 'none';
    canvas.style.display = 'block';
});

function sendImageToBackend(imageData) {
    console.log('Sending image data:', imageData);
    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        const resultElement = document.getElementById('result'); // Define resultElement
        resultElement.textContent = data.result; // Update the result element
        resultElement.style.display = 'block'; // Show the h2 element
    })
    .catch(error => {
        console.error('Error sending image to server:', error);
    });
}


