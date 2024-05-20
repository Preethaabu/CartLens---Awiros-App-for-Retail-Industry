

const express = require("express");
const app = express();
const fs = require("fs");
const path = require("path");
const fileUpload = require("express-fileupload");
const { spawn } = require("child_process");

app.use(express.static("public"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(fileUpload()); // Use the express-fileupload middleware

// Endpoint to handle image uploads
app.post("/upload-image", (req, res) => {
    if (!req.files || !req.files.image) {
        return res.status(400).json({ error: "No image file uploaded." });
    }

    const uploadedImage = req.files.image;
    const uploadDir = path.join(__dirname, "uploads");
    const uploadedImageName = `uploaded_${Date.now()}_${uploadedImage.name}`;
    const filePath = path.join(uploadDir, uploadedImageName);

    if (!fs.existsSync(uploadDir)) {
        fs.mkdirSync(uploadDir);
    }

    uploadedImage.mv(filePath, (err) => {
        if (err) {
            console.error("Error saving uploaded image:", err);
            return res.status(500).json({ error: "Failed to save uploaded image." });
        }

        console.log("Image saved:", uploadedImageName);
        // Run the Python script here
        const pythonScript = spawn('python', ['./ocr.py']);

        pythonScript.stdout.on("data", (data) => {
            console.log(`Python stdout: ${data}`);
        });

        pythonScript.stderr.on("data", (data) => {
            console.error(`Python stderr: ${data}`);
        });

        pythonScript.on("close", (code) => {
            console.log(`Python process exited with code ${code}`);
            // Send the generated image to the client
            //const generatedImagePath = "E:\\Projects\\object_detection\\data\\runs\\detect\\predict\\";
            //const imageName = uploadedImageName;
            // Update the src attribute of the <img> tag
            res.send({ imagePath: generatedImagePath + imageName });
        });
    });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});