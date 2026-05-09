import cv2
import pyttsx3
import speech_recognition as sr
import geocoder
import smtplib
from email.message import EmailMessage
import threading

# ----------- TEXT TO SPEECH -----------
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ----------- GET LOCATION -----------
def get_location():
    g = geocoder.ip('me')
    return g.latlng

# ----------- SEND EMAIL ALERT -----------
def send_email(location):
    EMAIL_ADDRESS = "jahnavirendla@gmail.com"
    EMAIL_PASSWORD = 'fyqhopvohuimjwdw'

    # 🔹 Create Google Maps link
    map_link = f"https://www.google.com/maps?q={location[0]},{location[1]}"

    msg = EmailMessage()
    msg['Subject'] = "🚨 EMERGENCY ALERT!"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = "shashanknamsani@gmail.com"

    # 🔹 Add link in message
    msg.set_content(f"""
HELP! I am in danger.

My location (coordinates): {location}

Open in Google Maps:
{map_link}
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email Sent!")
    except Exception as e:
        print("Error sending email:", e)

# ----------- CAMERA CAPTURE -----------       
def capture_image():
    import cv2
    import time

    cap = cv2.VideoCapture(0)
    time.sleep(2)

    if not cap.isOpened():
        print("Camera not opened!")
        return

    ret, frame = cap.read()

    if not ret or frame is None:
        print("Frame is empty!")
        cap.release()
        return

    cv2.imwrite("evidence.jpg", frame)
    print("Image Captured!")

    cap.release()
       
# ----------- VOICE DETECTION -----------
def listen_for_help():
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio).lower()
            print("You said:", text)

            if "help" in text or "save me" in text:
                trigger_alert()

        except:
            print("Could not understand")

# ----------- ALERT SYSTEM -----------
def trigger_alert():
    speak("Emergency alert activated")
    
    location = get_location()
    print("Location:", location)

    # 🔹 Create Google Maps link
    map_link = f"https://www.google.com/maps?q={location[0]},{location[1]}"
    print("Map Link:", map_link)

    capture_image()
    
    # 🔹 Send both location + map link
    send_email(location, map_link)
# ----------- MAIN FUNCTION -----------
def main():
    speak("Women safety system activated")

    # Run voice listener in background
    thread = threading.Thread(target=listen_for_help)
    thread.start()

    # Camera live feed
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Safety Camera", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Press 's' to trigger manually
        if cv2.waitKey(1) & 0xFF == ord('s'):
            trigger_alert()

    cap.release()
    cv2.destroyAllWindows()

# ----------- RUN PROJECT -----------
if __name__ == "__main__":
    main()
    