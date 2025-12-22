from customtkinter import *
from PIL import Image, ImageTk
import subprocess
import os
from in_out import in_out
from motion import noise
from rect_noise import rect_noise
from record import record
from find_motion import find_motion
from identify import maincall


app = CTk()
app.geometry("1280x720")
app.title("Hash&ke Smart CCTV Dashboard")
set_default_color_theme("dark-blue")


def run_object_detection():
    node_app_path = r"C:\Users\harsh\OneDrive\Desktop\RealTimeObjectDetectionTFJSReact"
    try:
        os.chdir(node_app_path)
        subprocess.Popen(["npm", "run", "start"], shell=True)
        print("Node.js application started successfully.")
    except Exception as e:
        print(f"Error running Node.js application: {e}")


app.configure(fg_color="#1A1A2E")


header_frame = CTkFrame(app, height=80, fg_color="#0F3460", corner_radius=10)
header_frame.pack(fill="x", pady=10)

header_label = CTkLabel(
    header_frame,
    text="Smart CCTV Dashboard",
    font=("Helvetica", 32, "bold"),
    text_color="white"
)
header_label.place(relx=0.5, rely=0.5, anchor="center")


icon_image = Image.open('icons/spy.png').resize((150, 150), Image.Resampling.LANCZOS)
icon_photo = ImageTk.PhotoImage(icon_image)
icon_label = CTkLabel(app, image=icon_photo, text="", fg_color="#1A1A2E")
icon_label.pack(pady=20)


button_frame = CTkFrame(app, fg_color="#162447", corner_radius=10)
button_frame.pack(pady=20, padx=20, fill="both", expand=True)

btn_icons = {
    "monitor": Image.open('icons/lamp.png').resize((40, 40), Image.Resampling.LANCZOS),
    "rectangle": Image.open('icons/rectangle-of-cutted-line-geometrical-shape.png').resize((40, 40), Image.Resampling.LANCZOS),
    "noise": Image.open('icons/security-camera.png').resize((40, 40), Image.Resampling.LANCZOS),
    "record": Image.open('icons/recording.png').resize((40, 40), Image.Resampling.LANCZOS),
    "in_out": Image.open('icons/incognito.png').resize((40, 40), Image.Resampling.LANCZOS),
    "exit": Image.open('icons/exit.png').resize((40, 40), Image.Resampling.LANCZOS),
    "identify": Image.open('icons/recording.png').resize((40, 40), Image.Resampling.LANCZOS),
    "object_detection": Image.open('icons/object.png').resize((40, 40), Image.Resampling.LANCZOS),
}

btn_icons = {key: ImageTk.PhotoImage(img) for key, img in btn_icons.items()}

buttons = [
    ("Monitor", find_motion, "#2D82B7", btn_icons["monitor"]),
    ("Rectangle", rect_noise, "#FF6F61", btn_icons["rectangle"]),
    ("Noise", noise, "#1FAA59", btn_icons["noise"]),
    ("Record", record, "#FFA41B", btn_icons["record"]),
    ("In Out", in_out, "#9D50BB", btn_icons["in_out"]),
    ("Identify", maincall, "#D72638", btn_icons["identify"]),
    ("Object Detection", run_object_detection, "#1B98E0", btn_icons["object_detection"]),
    ("Exit", app.destroy, "#E63946", btn_icons["exit"]),
]

for i, (text, cmd, color, icon) in enumerate(buttons):
    btn = CTkButton(
        master=button_frame,
        text=text,
        command=cmd,
        image=icon,
        compound="left",
        fg_color=color,
        hover_color="#3A4750",
        corner_radius=8,
        font=("Helvetica", 16, "bold")
    )
    btn.grid(row=i // 4, column=i % 4, padx=20, pady=20, sticky="nsew")

footer_label = CTkLabel(
    app,
    text="© Copyright Hash&ke | All Rights Reserved",
    font=("Verdana", 12),
    text_color="gray"
)
footer_label.pack(side="bottom", pady=10)

for i in range(2):
    button_frame.rowconfigure(i, weight=1)
for j in range(4):
    button_frame.columnconfigure(j, weight=1)

app.mainloop()
