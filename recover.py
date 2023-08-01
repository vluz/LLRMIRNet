import numpy as np
import keras
import time
import tensorflow as tf
import streamlit as st
from huggingface_hub import from_pretrained_keras
from PIL import Image


@st.cache_resource
def loadmodel():
    model = from_pretrained_keras("keras-io/lowlight-enhance-mirnet", compile=False)
    return model


@st.cache_resource
def infer(input):
    image = tf.keras.preprocessing.image.img_to_array(input)
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)
    output = model.predict(image)
    outputimage = output[0] * 255.0
    outputimage = outputimage.clip(0, 255)
    outputimage = outputimage.reshape((np.shape(outputimage)[0], np.shape(outputimage)[1], 3))
    outputimage = np.uint32(outputimage)
    return outputimage


st.title("Low Light Image Recovery")
st.divider()
model = loadmodel()
uploaded_file = st.file_uploader("Upload a 600x400 image to enhance", type= ['png', 'jpg'])
if uploaded_file:
    st.image(uploaded_file, caption='Original')
    if st.button("Attempt recover"):
        with st.spinner("Working..."):
            input = Image.open(uploaded_file).convert('RGB')
            enhancedimage = infer(input)
        st.image(enhancedimage, caption='Result')
    