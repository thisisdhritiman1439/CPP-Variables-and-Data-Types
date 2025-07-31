import streamlit as st
import os
import json
import hashlib
import uuid
import base64
import pyqrcode
import cv2
from PIL import Image
import numpy as np

# ------------------- Paths -----------------------
USER_DATA_FILE = "users.json"
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------- Helpers -----------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

def verify_image(img1_path, img2):
    try:
        img1 = Image.open(img1_path).resize((100, 100)).convert('L')
        img2 = img2.resize((100, 100)).convert('L')
        return np.allclose(np.array(img1), np.array(img2), atol=20)
    except:
        return False

# ------------------- UI Styling -----------------------

st.set_page_config(page_title="🔐 3-Level Auth System", layout="centered")

def header(text, size=24):
    st.markdown(f"<h3 style='font-size: {size}px;'>{text}</h3>", unsafe_allow_html=True)

# ------------------- Pages -----------------------

def register():
    header("📝 Register", 28)
    with st.form("RegisterForm"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        uploaded_file = st.file_uploader("Upload File to Protect", type=None)
        image = st.file_uploader("Upload Face Image (JPG/PNG)", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Register")

    if submit:
        if not all([email, password, uploaded_file, image]):
            st.error("All fields are required.")
            return
        if len(password) < 8:
            st.warning("Password must be at least 8 characters.")
            return

        users = load_users()
        if email in users:
            st.error("User already exists.")
            return

        uid = str(uuid.uuid4())
        user_folder = os.path.join(UPLOAD_FOLDER, uid)
        os.makedirs(user_folder, exist_ok=True)

        with open(os.path.join(user_folder, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())

        image_path = os.path.join(user_folder, "face.png")
        with open(image_path, "wb") as f:
            f.write(image.read())

        users[email] = {
            "password": hash_password(password),
            "file": uploaded_file.name,
            "uid": uid
        }
        save_users(users)

        st.success("Registered successfully. Please login!")

def login():
    header("🔐 Login", 28)
    with st.form("LoginForm"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Proceed to Factor 2")

    if submit:
        users = load_users()
        if email not in users or users[email]["password"] != hash_password(password):
            st.error("Invalid email or password.")
            return

        st.session_state["email"] = email
        show_qr_code(email)

def show_qr_code(email):
    st.info("Scan this QR code to get your 6-digit access code.")

    secret_code = str(uuid.uuid4().int)[:6]
    qr = pyqrcode.create(secret_code)
    qr_path = "qr.png"
    qr.png(qr_path, scale=5)

    with open("qr_secret.json", "w") as f:
        json.dump({"email": email, "code": secret_code}, f)

    st.image(qr_path)

    user_input = st.text_input("Enter 6-digit code from QR scan")

    if user_input:
        with open("qr_secret.json", "r") as f:
            qr_data = json.load(f)

        if qr_data["email"] == email and qr_data["code"] == user_input.strip():
            st.success("QR Verification Passed ✅")
            face_verification(email)
        else:
            st.error("Invalid QR Code. Restarting login...")
            st.session_state.clear()

def face_verification(email):
    st.info("Upload your registered face image for final verification.")

    uploaded_img = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        users = load_users()
        uid = users[email]["uid"]
        original_face = os.path.join(UPLOAD_FOLDER, uid, "face.png")
        img = Image.open(uploaded_img)

        if verify_image(original_face, img):
            st.success("Authentication successful ✅")

            file_name = users[email]["file"]
            file_path = os.path.join(UPLOAD_FOLDER, uid, file_name)

            with open(file_path, "rb") as f:
                btn = st.download_button("⬇️ Download Your Protected File", f, file_name)

            if btn:
                st.balloons()
        else:
            st.error("Face does not match! Restarting login...")
            st.session_state.clear()

# ------------------- Main -----------------------

def main():
    st.sidebar.markdown(
        "<h2 style='font-size:24px;'>🔐 3-Level Auth</h2>",
        unsafe_allow_html=True
    )
    choice = st.sidebar.radio("Navigation", ["Register", "Login", "Logout"])

    if choice == "Register":
        register()
    elif choice == "Login":
        login()
    elif choice == "Logout":
        st.session_state.clear()
        st.success("Logged out.")

if __name__ == "__main__":
    main()
