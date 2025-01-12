import tkinter as tk
import util
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
import subprocess
import datetime


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1100x520+350+100")
        
        # Apply dark mode theme
        util.set_dark_mode(self.main_window)

        # Create buttons and place them
        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'light blue', self.login)
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New User', 'grey', self.register_new_user, fg='black')
        self.login_button_main_window.place(x=750, y=300)
        self.register_new_user_button_main_window.place(x=750, y=400)

        # Create webcam label
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        
        self.add_webcam(self.webcam_label)

        # Directory setup for database and logs
        self.db_dir = './db'
        self.log_path = './log.txt'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        
        
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            
        self._label = label
        self.process_webcam()
        
        
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20, self.process_webcam)
        
        
    def login(self):
        unknown_img_path = './tmp.jpg'
        
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        
        try:
            # Call the face_recognition script and capture output
            output = subprocess.check_output(
                ['face_recognition', self.db_dir, unknown_img_path],
                text=True  # Ensures the output is a string (Python 3.7+)
            )
            name = output.split(',')[1].strip()
        except Exception as e:
            util.msg_box('Error', f'Face recognition failed: {str(e)}')
            return

        if name in ['no_persons_found', 'unknown_person']:
            util.msg_box('Error', 'No match found. Please register new user or try again...')
        else:
            util.msg_box('Success!', f'Welcome, {name}')
            with open(self.log_path, 'a') as f:
                f.write(f'{name} {datetime.datetime.now()}\n')
        
        os.remove(unknown_img_path)
    
    
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1100x520+370+120")
        
        # Apply dark mode to the new window
        util.set_dark_mode(self.register_new_user_window)
        
        # Create buttons and input fields
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'light blue', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)
    
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)
    
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        
        self.add_img_to_label(self.capture_label)
        
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)
        
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Enter your name:')
        self.text_label_register_new_user.place(x=750, y=70)
        
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()    
    
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
    
    def start(self):
        self.main_window.mainloop()
        
    def accept_register_new_user(self):
        # Get the name entered by the user and sanitize input
        name = self.entry_text_register_new_user.get("1.0", 'end-1c').strip()
        
        if name == '':
            util.msg_box('Error', 'Name cannot be empty')
            return

        # Define the path where the user image will be saved
        file_path = os.path.join(self.db_dir, f'{name}.jpg')

        if os.path.exists(file_path):
            overwrite = messagebox.askyesno(
                'User Exists',
                f'User "{name}" already exists. Do you want to overwrite their data?'
            )
            if not overwrite:
                util.msg_box('Action Cancelled', 'Registration cancelled. Please try again.')
                return

        # Save the user's image
        cv2.imwrite(file_path, self.register_new_user_capture)

        util.msg_box('Success!', f'User "{name}" registered successfully.')
    

if __name__ == "__main__":
    app = App()
    app.start()
