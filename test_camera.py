import #cv2

print("Checking cameras...")

for i in range(5):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    
    if cap is not None and cap.isOpened():
        print("Camera found at index", i)
        cap.release()
    else:
        print("No camera at index", i)