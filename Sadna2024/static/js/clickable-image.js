document.addEventListener("DOMContentLoaded", function() {
    // Get all elements with the class 'clickable-img'
    var clickableImages = document.querySelectorAll('.clickable-img');

    // Loop through each clickable image
    clickableImages.forEach(function(img) {
        // Add a click event listener to each image
        img.addEventListener('click', function() {
            // Get the ID of the clicked image
            var imgId = this.id;

            // Create a FormData object
            var formData = new FormData();
            formData.append('id', imgId);

            // Send a request to the backend with the form data
            fetch('/mark-as-taken', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json()) // Parse the JSON response
            .then(data => {
                // Display an alert with the response message
                alert(data.message); // Assuming the response has a 'message' field
                // Refresh the page
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
