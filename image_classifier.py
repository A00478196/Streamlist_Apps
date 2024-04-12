import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Load the pre-trained model
model = load_model("D:/MCDA/5580/Streamlit_Apps/mnist_digit_classifier")

# Function to preprocess the uploaded image
def preprocess_image(image):
    # Resize image to square shape (28x28 for MNIST)
    image = image.resize((28, 28))
    # Convert image to grayscale
    image = image.convert("L")
    # Convert image to numpy array
    image_array = np.array(image)
    # Normalize pixel values to range [0, 1]
    image_array = image_array / 255.0
    # Reshape image array to shape (1, 28, 28, 1) for model input
    image_array = np.reshape(image_array, (1, 28, 28, 1))
    return image_array

# Function to make prediction
def predict_digit(image):
    # Preprocess the image
    processed_image = preprocess_image(image)
    # Make prediction using the model
    prediction = model.predict(processed_image)
    # Get the predicted digit (index of maximum probability)
    digit = np.argmax(prediction)
    return digit

# Streamlit app
def main():
    st.title("Digit Classifier")
    st.write("Upload an image of a digit (0-9)")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Predict the digit
        digit = predict_digit(image)

        # Display the predicted digit
        st.write(f"Predicted Digit: {digit}")

if __name__ == "__main__":
    main()
