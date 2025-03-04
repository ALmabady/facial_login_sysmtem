import os
import tkinter as tk
from tkinter import messagebox
from deepface import DeepFace

def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=4,
                       width=26, font=("Arial", 18))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


from deepface import DeepFace
import os
import pickle

def recognize(img, db_path):
    try:
        result = DeepFace.find(img_path=img, db_path=db_path, enforce_detection=False)
        if len(result) == 0 or result[0].empty:
            return 'no_persons_found'
        else:
            match = result[0]['identity'].values[0]
            name = os.path.basename(match).split('.')[0]  # Assuming filenames are "name.jpg"
            return name
    except Exception as e:
        print(f"Error during recognition: {e}")
        return 'unknown_person'