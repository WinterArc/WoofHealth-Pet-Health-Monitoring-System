import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage

# Initialize the app
cred = credentials.Certificate(r"C:\Users\taash\Downloads\pethealth-firebase.json")
firebase_admin.initialize_app(cred, {'storageBucket': '<pethealth-e1fee.appspot.com>'})


# Get the image file from Firebase storage
bucket = storage.bucket()
blob = bucket.blob("gs://pethealth-e1fee.appspot.com/road.jpg")
url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')

# Display the image as the background
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url({url}) no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
