# ----------- IMPORTS -----------
import streamlit as st
import cv2
import smtplib
import geocoder
import speech_recognition as sr
from email.message import EmailMessage

# ----------- EMAIL FUNCTION -----------
def send_email(location_link):
    sender_email = "jahnavirendla@gmail.com"
# ----------- SEND EMAIL ALERT -----------
    sender_password = 'fyqhopvohuimjwdw'
    receiver_email = "devivamshi2005@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = "🚨 Emergency Alert"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msg.set_content(f"HELP! My location:\n{location_link}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

# ----------- LOCATION FUNCTION -----------
def get_location():
    g = geocoder.ip('me')
    lat, lng = g.latlng
    return f"https://www.google.com/maps?q={lat},{lng}"

# ----------- CAMERA FUNCTION -----------
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("capture.jpg", frame)
    cap.release()

# ----------- VOICE FUNCTION -----------
def listen_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... say 'save me'")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except:
        return ""

# ----------- STREAMLIT UI -----------

st.title("🚨 Women Safety AI System")

st.header("Emergency Controls")

# 🔴 ALERT BUTTON
if st.button("🚨 Send Alert"):
    st.warning("Alert Triggered!")

    location_link = get_location()
    capture_image()
    send_email(location_link)

    st.success("Email Sent Successfully!")

# 🎤 VOICE BUTTON
if st.button("🎤 Voice Alert"):
    text = listen_voice()

    if "save me" in text:
        st.warning("Voice Alert Detected!")

        location_link = get_location()
        capture_image()
        send_email(location_link)

        st.success("Alert Sent via Voice!")
    else:
        st.error("No valid command detected")

# 📷 CAMERA BUTTON
if st.button("📷 Capture Image"):import os

# ... all your other code (routes, logic, etc.) ...
    capture_image()
    st.success("Image Captured Successfully!")
import os

if __name__ == "__main__":
    # Get the port from Railway's environment, or use 5000 as a backup
    port = int(os.environ.get("PORT", 5000))
    # 0.0.0.0 is CRITICAL—it tells the app to listen to the whole internet
    app.run(host="0.0.0.0", port=port)
