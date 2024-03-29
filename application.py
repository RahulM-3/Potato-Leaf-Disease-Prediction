import streamlit as st
from PIL import Image
import os
import datetime

import keras
import numpy as np

from google_gemini import getsolution

checkfolder = r"automatefolder"
report = {}

def predict_class(image) :
    classifier_model = keras.models.load_model(r'classification.keras', compile = False)
    image = Image.open(image)
    #shape = ((256,256,3))
    test_image = image.resize((256, 256))
    test_image = keras.preprocessing.image.img_to_array(test_image)
    test_image /= 255.0
    test_image = np.expand_dims(test_image, axis = 0)
    class_name = ['Early blight',  'Healthy', 'Late blight',]

    prediction = classifier_model.predict(test_image)
    confidence = round(100 * (np.max(prediction[0])), 2)
    final_pred = class_name[np.argmax(prediction)]
    return final_pred, str(confidence), prediction


txt = st.empty()
admin = st.empty()
user = st.empty()

asadmin = False
asuser = False
if("loggedin" not in st.session_state):
    txt.write("Access the page as")
    asadmin = admin.button("Admin")
    asuser = user.button("User")
else:
    if(st.session_state["loggedin"] == "admin"):
        asadmin = True
    else:
        asuser = True

if(asuser):
    st.session_state["loggedin"] = "user"
    admin.empty()
    user.empty()
    txt.empty()

    files = st.file_uploader("upload leaf image", type=["png", "jpg"], accept_multiple_files=True)
    discol = st.columns(2)
    for i, f in enumerate(files):
        with discol[i%2]:
            st.image(f)
            data = predict_class(f)
            with st.container(border=True):
                st.write(f"**State:**", data[0])
                st.write(f"**Probability:**", data[1])
                st.write(getsolution(data))

elif(asadmin):
    st.session_state["loggedin"] = "admin"
    txt.empty()
    admin.empty()
    user.empty()

    st.write("Set Automation time")
    timesolc = st.columns(2)
    with timesolc[0]:
        start = st.time_input(label="Start", step=600)
    with timesolc[1]:
        end = st.time_input(label="End", step=600)
    hrs = end.hour-start.hour
    min = abs(end.minute-start.minute)
    if(hrs < 0):
        st.write("End time should be after start time")
    if(hrs > 0):
        st.write(f"**Automation set for:** {hrs}:{min}")
        stop = st.button(label="Stop")
        image_extensions = [".jpg", ".jpeg", ".png"]
        discol = st.columns(2)
        i = 0
        while(datetime.datetime.now().hour <= start.hour and datetime.datetime.now().minute <= end.minute):
            for filename in os.listdir(checkfolder):
                if(any(filename.lower().endswith(ext) for ext in image_extensions) and filename not in report):
                    with discol[i%2]:
                        st.image(f"automatefolder\{filename}")
                        data = predict_class(f"automatefolder\{filename}")
                        report[filename] = data
                        with st.container(border=True):
                            st.write(f"**State:**", data[0])
                            st.write(f"**Probability:**", data[1])
                            st.write(getsolution(data))
                    i+=1
            if(stop):
                st.write(report)
                break