function fetchData() {
  fetch('/get_data')
    .then(response => response.json())
    .then(data => {
      // Get the container
      let container = document.getElementById('data-container');
      // Clear previous content
      container.innerHTML = "";
      if (data) {
        let message = document.createElement('div');
        message.className = 'message ' + (data.username === 'nikechan' ? 'message-left' : 'message-right');
        // message.textContent = `username: ${data.username}, timestamp: ${data.timestamp}, message: ${data.message}`;
        message.textContent = data.message;
        container.appendChild(message);
      }
    })
    .catch(error => console.error('Error:', error));
}

// Fetch data every 2 seconds
setInterval(fetchData, 2000);
