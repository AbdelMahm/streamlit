import streamlit as st
import pandas as pd
import numpy as np
import cv2
import datetime
import mss


st.title('Deepecho Video Analyzer')
#controls
st.sidebar.title("Controls")
btn_start = st.sidebar.button("Start", key=1)
btn_stop = st.sidebar.button("Stop", key=2)
uploaded_file = st.sidebar.file_uploader("Choose a video file", key="video_file")
   
# bounding box
top = 0
left = 0
frame_width = 500
frame_height = 500

#frame rate
frame_rate = 20.0

# output filename
time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
file_name = f'{time_stamp}.mp4'
#file_name = 'record.mp4'

# video encoding
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # (*'MP4V')
video_writer = cv2.VideoWriter(file_name, fourcc, frame_rate, (frame_width, frame_height))

if 'start' not in st.session_state:
    st.session_state.start = 1

st.session_state.start = 1

#mss to capture screen
with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": top, "left": left, "width": frame_width, "height": frame_height}

    while st.session_state.start == 1:
        
        st.write("recording...")
        
        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))
        img = cv2.resize(img, (frame_width, frame_height))
        frame = img # initialize frame

        #convert to RGB
        frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #write to video file
        video_writer.write(frame)
        
        if btn_stop:
            st.session_state.start = 2
            st.write("stop.")
            st.stop()
   
# Clean up
video_writer.release()
cv2.destroyAllWindows()

if uploaded_file is not None:
    # To read file as bytes:
    #bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)
    print(uploaded_file.name)

    # show the video
    video_file = open(uploaded_file.name, 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)
