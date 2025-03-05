import os
from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import rasterio
from PIL import Image
import io
from pyngrok import ngrok

# Initialize Flask app
app = Flask(__name__)

# Define paths
UPLOAD_FOLDER = 'uploads/'
MODEL_PATH = 'water_segmentation_model.h5'

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained model
model = tf.keras.models.load_model(MODEL_PATH)

# Function to preprocess the image
def preprocess_image(image):
    # Read the image using rasterio
    with rasterio.open(io.BytesIO(image)) as img:
        image_data = img.read()  # Shape: (num_bands, 128, 128)
        image_data = np.transpose(image_data, (1, 2, 0))  # Shape: (128, 128, num_bands)
    
    # Normalize the image (if required)
    image_data = image_data / 10000.0  # Adjust based on your normalization scheme
    
    # Add batch dimension
    image_data = image_data[np.newaxis, ...]
    
    return image_data

# Function to generate the predicted mask
def predict_mask(image):
    pred_mask = model.predict(image)
    pred_mask = (pred_mask > 0.5).astype(np.uint8)  # Convert to binary mask
    return pred_mask[0, :, :, 0]  # Remove batch dimension

# API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Read the uploaded file
    image = file.read()
    
    try:
        # Preprocess the image
        image_data = preprocess_image(image)
        
        # Generate the predicted mask
        mask = predict_mask(image_data)
        
        # Convert the mask to a PNG image
        mask_image = Image.fromarray(mask * 255)  # Scale to 0-255
        mask_bytes = io.BytesIO()
        mask_image.save(mask_bytes, format='PNG')
        mask_bytes.seek(0)
        
        # Return the predicted mask as a response
        return mask_bytes.getvalue(), 200, {'Content-Type': 'image/png'}
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app with ngrok
if __name__ == '__main__':
    # Start ngrok and create a tunnel to the Flask app
    public_url = ngrok.connect(5000).public_url
    print(f" * Running on {public_url}")
    
    # Run the Flask app
    app.run()