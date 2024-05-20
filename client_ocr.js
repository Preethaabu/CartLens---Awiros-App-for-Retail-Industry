// Wrap your code inside DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", function () {
    // Add an event listener to handle image upload
    document.getElementById("uploadImage").addEventListener("click", function (e) {
        e.preventDefault(); // Prevent the default form submission behavior

        const imageInput = document.getElementById("imageInput");
        const selectedImage = imageInput.files[0];

        if (!selectedImage) {
            console.error("No image selected.");
            return;
        }

        const formData = new FormData();
        formData.append("image", selectedImage);

        fetch("http://localhost:3000/upload-image", {
            method: "POST",
            body: formData,
        })
        .then(function (response) {
            if (response.status === 200) {
                console.log("Image uploaded successfully");

                // Parse the JSON response to get the image path
                response.json().then(function (data) {
                    const generatedImageElement = document.getElementById("generatedImage");
                    generatedImageElement.src = data.imagePath; // Set the src attribute
                    generatedImageElement.style.display = "block"; // Make sure the image is visible
                });
            } else {
                console.error("Error uploading image:", response.statusText);
            }
        })
        .catch(function (error) {
            console.error("Error uploading image:", error);
        });
    });
});
