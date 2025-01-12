import os
import pickle
import tkinter as tk
from tkinter import messagebox
import face_recognition


# Function to create modern buttons with rounded edges and hover effect in dark mode
def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground=color,
        activeforeground=fg,
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=15,
        font=('Times New Roman', 14, 'bold'),
        relief='flat',
        bd=0,
        padx=10,
        pady=10,
        borderwidth=2,
        highlightthickness=0
    )

    # Hover effect
    button.bind("<Enter>", lambda e: button.config(bg='lightblue'))  # Change to lighter color on hover
    button.bind("<Leave>", lambda e: button.config(bg=color))  # Reset to original color on leave

    return button


# Function to create image labels with a dark background
def get_img_label(window):
    label = tk.Label(window, bd=2, relief='solid', width=100, height=30, bg='#2E2E2E')
    label.grid(row=0, column=0, padx=20, pady=20)
    return label


# Function to create styled text labels with dark theme
def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Segoe UI", 18, 'bold'), justify="left", fg="#FFFFFF", bg="#2E2E2E")
    return label


# Function to create entry text fields with a dark theme
def get_entry_text(window):
    inputtxt = tk.Text(window, height=2, width=20, font=("Segoe UI", 18), bd=2, relief='solid', bg='#4D4D4D', fg='#FFFFFF')
    return inputtxt


# Function to display message boxes with a professional dark mode design
def msg_box(title, description):
    messagebox.showinfo(title, description)


# Face recognition function (same as before)
def recognize(img, db_path):
    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'


# Function to set up the dark mode theme for the entire window
def set_dark_mode(window):
    window.config(bg="#2E2E2E")  # Dark background color for the main window
    window.tk_setPalette(background='#2E2E2E', foreground='white', activeBackground='lightblue', activeForeground='white')
