import streamlit as st
from PIL import Image
import numpy as np
import mlflow
import cv2
import os

@st.cache_resource
def load_model(filepath):
    import keras  
    model = keras.saving.load_model(filepath, custom_objects=None, compile=True, safe_mode=True)
    return model

model = load_model(filepath = os.path.join(os.getcwd(),'models','model.keras'))

st.title("Concrete Cracks Detector")
uploaded_file = st.file_uploader("Upload image here", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

    if st.button("Submit"):
        img = np.array(image)
        img = cv2.resize(img, dsize=(160,160))
        img = np.expand_dims(img, axis=0)
        st.success("Image submitted!")
        classes = ['Negative', 'Positive']
        pred = np.argmax(model.predict(img),axis=1)
        predicted_class = classes[int(pred)]
        st.header(f"Result: {predicted_class}")
        if predicted_class == 'Negative':
            st.write("There is no crack on the sample.")
        elif predicted_class == 'Positive':
            st.write("The sample is cracked")
        else:
            st.error('Model returns unexpected outcome')