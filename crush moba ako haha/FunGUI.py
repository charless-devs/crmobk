import tkinter as tk
from PIL import Image, ImageTk
import random
import vlc
import os

# Paths
IMAGE_PATH = "OIP (1).jpg"
VIDEO_PATH = "Tagumpay.mp4"

root = tk.Tk()
root.title("Kupal workspace")
root.geometry("600x500")

# Top message
message_label = tk.Label(root, text="GUSTO MOBA TALAGA AKO??", font=("Arial", 24))
message_label.pack(pady=10)

# Center frame for image/video
media_frame = tk.Frame(root, width=400, height=250)
media_frame.pack(pady=20)

# Show image initially
img = Image.open(IMAGE_PATH)
img = img.resize((400, 250))
photo = ImageTk.PhotoImage(img)
image_label = tk.Label(media_frame, image=photo)
image_label.pack()

# VLC instance
instance = vlc.Instance()
player = instance.media_player_new()

# Canvas for buttons
canvas = tk.Canvas(root, width=600, height=100, highlightthickness=0)
canvas.pack(side=tk.BOTTOM)

# Draw a rounded button with text
def draw_rounded_button(x, y, w, h, r, color, text, command=None):
    # Rounded rectangle: 4 arcs + 2 rectangles
    parts = []
    parts.append(canvas.create_arc(x, y, x+2*r, y+2*r, start=90, extent=90, fill=color, outline=color))
    parts.append(canvas.create_arc(x+w-2*r, y, x+w, y+2*r, start=0, extent=90, fill=color, outline=color))
    parts.append(canvas.create_arc(x, y+h-2*r, x+2*r, y+h, start=180, extent=90, fill=color, outline=color))
    parts.append(canvas.create_arc(x+w-2*r, y+h-2*r, x+w, y+h, start=270, extent=90, fill=color, outline=color))
    parts.append(canvas.create_rectangle(x+r, y, x+w-r, y+h, fill=color, outline=color))
    parts.append(canvas.create_rectangle(x, y+r, x+w, y+h-r, fill=color, outline=color))
    text_id = canvas.create_text(x+w/2, y+h/2, text=text, fill="white", font=("Arial", 12, "bold"))
    parts.append(text_id)
    btn = {"x": x, "y": y, "w": w, "h": h, "r": r, "color": color, "text_id": text_id, "parts": parts, "command": command}
    return btn

# Check if mouse is inside button
def is_inside(btn, mx, my):
    return btn["x"] <= mx <= btn["x"] + btn["w"] and btn["y"] <= my <= btn["y"] + btn["h"]

# Move No/Maybe buttons on hover
def on_mouse_move(event):
    for btn in [no_btn, maybe_btn]:
        if is_inside(btn, event.x, event.y):
            # Move randomly
            new_x = random.randint(0, 600 - btn["w"])
            new_y = random.randint(0, 100 - btn["h"])
            dx = new_x - btn["x"]
            dy = new_y - btn["y"]
            for part in btn["parts"]:
                canvas.move(part, dx, dy)
            btn["x"] = new_x
            btn["y"] = new_y

# Click detection
def on_click(event):
    for btn in [yes_btn, no_btn, maybe_btn]:
        if is_inside(btn, event.x, event.y) and btn["command"]:
            btn["command"]()

canvas.bind("<Motion>", on_mouse_move)
canvas.bind("<Button-1>", on_click)

# Function to play video in place of image
def play_video_in_place():
    # Remove image
    image_label.pack_forget()
    # Create a canvas for video
    video_canvas = tk.Canvas(media_frame, width=400, height=250)
    video_canvas.pack()
    media = instance.media_new(VIDEO_PATH)
    player.set_media(media)

    if os.name == "nt":  # Windows
        player.set_hwnd(video_canvas.winfo_id())
    else:  # Mac/Linux
        player.set_xwindow(video_canvas.winfo_id())

    player.play()

# Create buttons
yes_btn = draw_rounded_button(100, 20, 100, 40, 20, "red", "Yes", play_video_in_place)
no_btn = draw_rounded_button(250, 20, 100, 40, 20, "blue", "No")
maybe_btn = draw_rounded_button(400, 20, 100, 40, 20, "green", "Maybe")

root.mainloop()
