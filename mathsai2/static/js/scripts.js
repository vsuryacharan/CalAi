window.onload = function () {
    const canvas = document.getElementById('mathCanvas');
    const ctx = canvas.getContext('2d');
    let drawing = false;

    // Function to start drawing
    function startDrawing(e) {
        drawing = true;
        draw(e);
    }

    // Function to stop drawing
    function stopDrawing() {
        drawing = false;
        ctx.beginPath(); // Ensures that separate lines are drawn
    }

    // Function to handle the drawing on the canvas
    function draw(e) {
        if (!drawing) return;

        // Set line properties
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'black';

        // Get the mouse position relative to the canvas
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Draw the line
        ctx.lineTo(x, y);
        ctx.stroke();

        // Begin a new path for the next segment
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    // Add event listeners for mouse actions
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mousemove', draw);

    // Handle button click to submit the image to the server
    document.getElementById('submit-btn').addEventListener('click', function () {
        // Convert canvas content to base64 image
        const dataURL = canvas.toDataURL('image/png');

        // Display the captured image in the image preview element
        const imagePreview = document.getElementById('image-preview');
        imagePreview.src = dataURL;
        imagePreview.style.display = 'block'; // Show the image preview

        // Send the image to the Flask backend for analysis
        fetch('/solve-equation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: dataURL }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = JSON.stringify(data);
        })
        .catch(error => console.error('Error:', error));
    });
};
