// Date and time
document.addEventListener("DOMContentLoaded", function () {
    const datetimeDisplay = document.getElementById("datetime-display");

    // Function to update the date and time
    function updateDateTime() {
        const now = new Date();
        const formattedDateTime = now.toLocaleString(); // Format: e.g., "12/7/2024, 2:45:23 PM"
        datetimeDisplay.textContent = `Current Date and Time: ${formattedDateTime}`;
    }

    // Update date and time every second
    setInterval(updateDateTime, 1000);
    updateDateTime(); // Initial call to display immediately
});

// Toggle switch
document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitch = document.getElementById("toggle-switch");
    const ws = new WebSocket("ws://192.168.1.93:8888");

    ws.onopen = function () {
        console.log("WebSocket connection established");
    };

    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        toggleSwitch.checked = data.state; // Update the toggle switch based on server state
    };

    ws.onerror = function (error) {
        console.error("WebSocket error:", error);
    };

    ws.onclose = function () {
        console.log("WebSocket connection closed");
    };

    // Handle switch toggle
    toggleSwitch.addEventListener("change", function () {
        const currentState = toggleSwitch.checked;

        // Send the updated state to the server via WebSocket
        ws.send(JSON.stringify({ state: currentState }));
    });
});
