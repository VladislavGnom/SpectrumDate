const socket = new WebSocket(
    `ws://${window.location.host}/ws/online-status/`
);

socket.onopen = function(e) {
    console.log("WebSocket connected");
};

socket.onclose = function(e) {
    console.log("WebSocket disconnected");
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Status update:", data);
};
