// Date and time
document.addEventListener("DOMContentLoaded", function () {
    const datetimeDisplay = document.getElementById("datetime-display");

    function updateDateTime() {
        const now = new Date();
        const formattedDateTime = new Intl.DateTimeFormat('it-IT', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false, // Use 24-hour format
        }).format(now);
    
        datetimeDisplay.textContent = `Data e ora attuale: ${formattedDateTime}`;
    }    

    // Update date and time every second
    setInterval(updateDateTime, 1000);
    updateDateTime(); // Initial call to display immediately
});

// Toggle switch
document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitch = document.getElementById("toggle-switch");
    const capturingText = document.getElementById("capturing-text");
    const imageTimestamp = document.getElementById("image-timestamp");
    const ws = new WebSocket("ws://192.168.1.93:8888");

    let isCapturing = false;

    ws.onopen = function () {
        console.log("WebSocket connection established");
    };

    ws.onmessage = async function (event) {
        const data = JSON.parse(event.data);
        toggleSwitch.checked = data.state; // Update the toggle switch based on server state

        if (!data.state) {
            capturingText.style.display = "none"; // Hide "Capturing..." when OFF
        }

        // Fetch the timestamp when the capture is completed
        if (data.state === false) {
            try {
                const response = await fetch("/time.txt");
                const timestamp = await response.text();
                imageTimestamp.textContent = `Ultima immagine scattata il: ${timestamp.trim()}`;
            } catch (error) {
                console.error("Error fetching timestamp:", error);
            }
        }
    };

    ws.onerror = function (error) {
        console.error("WebSocket error:", error);
    };

    ws.onclose = function () {
        console.log("WebSocket connection closed");
    };

    // Handle switch toggle
    toggleSwitch.addEventListener("change", function () {
        if (isCapturing) {
            return;
        }

        const currentState = toggleSwitch.checked;

        // Display "Capturing..." when ON
        if (currentState) {
            capturingText.style.display = "block";
        }

        // Disable the toggle switch while capturing
        toggleSwitch.disabled = true;
        isCapturing = true;

        // Send the updated state to the server via WebSocket
        ws.send(JSON.stringify({ state: currentState }));

        // Simulate a capture process
        setTimeout(() => {
            isCapturing = false; // Reset capturing state
            toggleSwitch.disabled = false; // Re-enable the toggle switch
            if (!currentState) {
                capturingText.style.display = "none";
            }
        }, 7000); // Adjust based on actual capture time
    });
});

// Video stream and timestamp update
document.addEventListener("DOMContentLoaded", function () {
    const videoStream = document.getElementById("video-stream");
    const imageTimestamp = document.getElementById("image-timestamp");

    function fetchFrameAndTimestamp() {
        const timestampUrl = `/time.txt?nocache=${new Date().getTime()}`; // Cache-busting URL

        // Fetch the latest frame
        fetch("/image_frame")
            .then((response) => {
                if (response.ok) {
                    return response.blob();
                }
                throw new Error("Failed to fetch frame");
            })
            .then((blob) => {
                videoStream.src = URL.createObjectURL(blob);
            })
            .catch((error) => {
                console.error("Error fetching frame:", error);
            });

        // Fetch the latest timestamp
        fetch(timestampUrl)
            .then((response) => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error("Failed to fetch timestamp");
            })
            .then((timestamp) => {
                imageTimestamp.textContent = `Ultima immagine scattata il: ${timestamp.trim()}`;
            })
            .catch((error) => {
                console.error("Error fetching timestamp:", error);
            });
    }

    // Update the video stream and timestamp periodically
    setInterval(fetchFrameAndTimestamp, 1000);
});
