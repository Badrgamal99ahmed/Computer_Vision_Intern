import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load Model
model = tf.keras.models.load_model("teeth_classification_model.h5")

# Class Labels
class_labels = ["Cas", "Cos", "Gum", "MC", "OC", "OLP", "OT"]

# Streamlit App
st.title("Teeth Disease Classification")
st.write("Upload an image of a tooth, and the AI will classify the disease.")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).resize((256, 256))
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess Image
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    predicted_class = class_labels[np.argmax(prediction)]
    confidence = np.max(prediction)

    # Display Prediction
    st.write(f"### Prediction: {predicted_class}")
    st.write(f"Confidence: {confidence:.2f}")
