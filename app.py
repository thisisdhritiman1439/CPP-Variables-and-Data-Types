import streamlit as st
import pandas as pd
import os
import time
import random
import pyqrcode
import cv2
import base64
from datetime import datetime

# CSV file for user database
USER_DB = "users.csv"
LOGIN_LOG = "login_log.csv"

# Ensure CSV files exist
if not os.path.exists(USER_DB):
    pd.DataFrame(columns=["email", "password", "image", "secret_code"]).to_csv(USER_DB, index=False)
if not os.path.exists(LOGIN_LOG):
    pd.DataFrame(columns=["email", "login_time"]).to_csv(LOGIN_LOG, index=False)

# ---------- Helper Functions ----------

def save_user(email, password, uploaded_file, secret_code):
    file_path = f"images/{email.replace('@', '_at_')}.jpg"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    df = pd.read_csv(USER_DB)
    df = df.append({"email": email, "password": password, "image": file_path, "secret_code": secret_code}, ignore_index=True)
    df.to_csv(USER_DB, index=False)

def validate_credentials(email, password):
    df = pd.read_csv(USER_DB)
    user = df[(df.email == email) & (df.password == password)]
    return not user.empty

def get_user_info(email):
    df = pd.read_csv(USER_DB)
    user = df[df.email == email].iloc[0]
    return user

def generate_qr_code(code):
    qr = pyqrcode.create(code)
    qr.png("qr.png", scale=6)
    return "qr.png"

def facial_match(stored_image_path):
    st.info("Turn on your webcam and align your face")
    cap = cv2.VideoCapture(0)
    stframe = st.empty()
    matched = False

    for _ in range(50):
        ret, frame = cap.read()
        if not ret:
            break

        stframe.image(frame, channels="BGR")

        cv2.imwrite("current.jpg", frame)
        match_score = compare_images("current.jpg", stored_image_path)

        if match_score >= 0.6:
            matched = True
            break
    cap.release()
    return matched

def compare_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        return 0

    img1 = cv2.resize(img1, (100, 100))
    img2 = cv2.resize(img2, (100, 100))

    diff = cv2.absdiff(img1, img2)
    score = 1 - (cv2.countNonZero(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)) / (100 * 100))
    return score

def record_login(email):
    df = pd.read_csv(LOGIN_LOG)
    df = df.append({"email": email, "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, ignore_index=True)
    df.to_csv(LOGIN_LOG, index=False)

# ---------- App UI ----------

st.set_page_config(page_title="Three-Factor Authentication", layout="centered")
st.title("🔐 Three-Factor Authentication System")
st.markdown("<h3 style='font-size:22px;'>Secure your login with Email + QR + Face Recognition</h3>", unsafe_allow_html=True)

menu = ["Login", "Register"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Register":
    st.subheader("📥 Register")
    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        uploaded_file = st.file_uploader("Upload your face image", type=["jpg", "jpeg", "png"])
        secret_code = str(random.randint(100000, 999999))
        submitted = st.form_submit_button("Register")

        if submitted:
            if email and password and uploaded_file:
                save_user(email, password, uploaded_file, secret_code)
                st.success("Registered successfully!")
                st.image(generate_qr_code(secret_code), caption="Scan this QR for 6-digit code")
            else:
                st.error("Please fill all fields and upload a face image.")

elif choice == "Login":
    st.subheader("🔐 Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if validate_credentials(email, password):
            st.success("✅ Step 1 Passed: Email and Password matched")
            user = get_user_info(email)
            qr_code_path = generate_qr_code(user['secret_code'])
            st.image(qr_code_path, caption="Scan QR and enter the 6-digit code")
            code = st.text_input("Enter the code visible from QR")

            if code == user['secret_code']:
                st.success("✅ Step 2 Passed: QR code matched")

                if facial_match(user['image']):
                    st.success("✅ Step 3 Passed: Facial Recognition Successful")
                    record_login(email)
                    st.balloons()
                    st.info(f"Access granted to secure files for: {email}")
                    st.write("Here are your protected files:")
                    uploaded_files = st.file_uploader("Upload or View Your Files", accept_multiple_files=True)
                    for file in uploaded_files:
                        st.write(f"- {file.name}")
                else:
                    st.error("❌ Step 3 Failed: Face doesn't match")
            else:
                st.error("❌ Step 2 Failed: Incorrect code")
        else:
            st.error("❌ Step 1 Failed: Incorrect email or password")
