from customtkinter import *
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
from tkinter import simpledialog
from datetime import datetime

os.makedirs(r"C:\Users\harsh\OneDrive\Desktop\smart-cctv-ver2.0\persons", exist_ok=True)

f_cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

set_appearance_mode("Dark")
set_default_color_theme("dark-blue")

def collect_data():
    name = simpledialog.askstring("Input", "Enter name of the person:")
    if not name:
        print("No name entered. Data collection canceled.")
        return

    ids = simpledialog.askstring("Input", "Enter ID:")
    if not ids:
        print("No ID entered. Data collection canceled.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    count = 0
    while count < 300:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = f_cas.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = gray[y:y + h, x:x + w]
            img_path = f"C:/Users/harsh/OneDrive/Desktop/smart-cctv-ver2.0/persons/{name}-{count + 1}-{ids}.jpg"
            cv2.imwrite(img_path, roi)
            print(f"Saved: {img_path}")
            count += 1
            if count >= 300:
                break

        cv2.imshow("Data Collection", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Data collection complete.")
    train()

def train():
    print("Training the model...")
    recog = cv2.face.LBPHFaceRecognizer_create()
    dataset = r"C:\Users\harsh\OneDrive\Desktop\smart-cctv-ver2.0\persons"
    paths = [os.path.join(dataset, img) for img in os.listdir(dataset)]
    faces, ids = [], []

    for path in paths:
        img = cv2.imread(path, 0)
        try:
            label = int(os.path.basename(path).split('-')[2].split('.')[0])
            ids.append(label)
            faces.append(img)
        except (IndexError, ValueError):
            print(f"Skipping invalid image: {path}")
            continue

    recog.train(faces, np.array(ids))
    recog.save('model.yml')
    print("Training completed and model saved as model.yml.")

def identify():
    print("Identifying...")
    recog = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists('model.yml'):
        recog.read('model.yml')
    else:
        print("Model not found. Please run 'train()' first.")
        return

    dataset = r"C:\Users\harsh\OneDrive\Desktop\smart-cctv-ver2.0\persons"
    paths = [os.path.join(dataset, img) for img in os.listdir(dataset)]
    labelslist = {}

    for img in paths:
        try:
            parts = os.path.basename(img).split('-')
            if len(parts) > 2:
                label = parts[2].split('.')[0]
                name = parts[0]
                labelslist[label] = name
        except IndexError:
            print(f"Skipping invalid image: {img}")
            continue

    attendance_logged = {}
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = f_cas.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = gray[y:y + h, x:x + w]
            label, confidence = recog.predict(roi)

            if confidence < 100:
                name = labelslist.get(str(label), "Unknown")
                if name not in attendance_logged:
                    log_attendance(name)
                    attendance_logged[name] = True
                cv2.putText(frame, f"{name} ({int(confidence)})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Identify", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def maincall():
    app = CTk()
    app.geometry("600x300")
    app.title("Face Recognition Menu")

    header = CTkLabel(app, text="Smart CCTV Face Recognition", font=("Helvetica", 24, "bold"), text_color="white")
    header.pack(pady=20)

    buttons = [
        ("Add Member", collect_data),
        ("Identify Member", identify),
        ("Start Live Transmission", live_transmission),
    ]

    for text, command in buttons:
        btn = CTkButton(app, text=text, command=command, font=("Helvetica", 16), fg_color="#0F3460", hover_color="#1A508B")
        btn.pack(pady=10, fill="x", padx=50)

    app.mainloop()

def log_attendance(name):
    try:
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        attendance_file = r"C:\Users\harsh\OneDrive\Desktop\smart-cctv-ver2.0\persons\attendance_log.txt"

        with open(attendance_file, "a") as file:
            file.write(f"Name: {name}, Date: {date}, Time: {time}\n")

        print(f"Attendance for {name} recorded at {date} {time}")
    except Exception as e:
        print(f"Error logging attendance: {e}")

def live_transmission():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = f_cas.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

        cv2.imshow("Live Transmission", frame)
        if cv2.waitKey(5) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    maincall()
