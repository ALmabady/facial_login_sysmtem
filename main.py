# this is the main file for the face login system 

# the libraries we need :
import os
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk

class App():
    # constructor 
    def __init__(self):
        #calling the main window function
        self.main_window_func()

        # dir to save photos from registered people
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    # --> main window function
    def main_window_func(self):
        #main window
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+280+100")

        #login button 
        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x = 750, y = 300)

        #regitser button ( take a new photo )
        self.register_button_main_window = util.get_button(self.main_window, 'Register \n ( take a photo )' , 'gray', self.register_new_user , fg='black')
        self.register_button_main_window.place(x = 750, y = 400)

        #main window webcam label 
        self.webcam_label_main_window = util.get_img_label(self.main_window)
        self.webcam_label_main_window.place(x = 10 , y = 0 ,width = 700, height= 500)

        #streaming webcam captured images
        self.add_webcam(self.webcam_label_main_window)

    # add webcam for main window
    def add_webcam(self,label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        
        self.label = label 
        self.process_webcam()

    # process webcam for main window
    def process_webcam(self):

        _ , frame = self.cap.read()
        self.recent_captured_arr = frame

        #converting from bgr to rgb and then to pil 
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        self.recent_captured_pil = img

        #configuring the pil image and display it
        imgtk = ImageTk.PhotoImage(img)
        self.label.imgtk = imgtk
        self.label.configure(image = imgtk)
        self.label.after(20,self.process_webcam)


    def login(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.recent_captured_arr.copy())
        
        name = util.recognize(unknown_img_path, self.db_dir)
        
        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups ...', 'Unknown user. Please register new user OR try again.')
        else:
            util.msg_box('Welcome back!', f'Welcome, {name}')

        os.remove(unknown_img_path)
    
    # --> register new user window
    def register_new_user(self):
        #window 
        self.new_user_window = tk.Toplevel(self.main_window)
        self.new_user_window.geometry("1200x520+300+120")

        #accept button 
        self.accept_button_new_user_window = util.get_button(self.new_user_window, 'Accept', 'green', self.accept_new_user)
        self.accept_button_new_user_window.place(x = 750, y = 300)

        #Try agian button
        self.try_again_button_new_user_window = util.get_button(self.new_user_window, 'Try agian \n ( take another photo )', 'red', self.try_agian_new_user)
        self.try_again_button_new_user_window.place(x = 750, y = 400)

        # new user capture label
        self.capture_label_new_user = util.get_img_label(self.new_user_window)
        self.capture_label_new_user.place(x = 10 , y = 0 ,width = 700, height= 500)

        # one image captured 
        self.add_img_to_label(self.capture_label_new_user)

        #user name 
        self.new_user_name = util.get_entry_text(self.new_user_window) # to input the text from the user
        self.new_user_name.place(x = 750, y = 150)

        self.label_above_box_user_window = util.get_text_label(self.new_user_window ,'Please, Input UserName :') # the label above input box
        self.label_above_box_user_window.place(x = 750, y = 70)
        


    #trying again and capturing new photo for the user
    def try_agian_new_user(self):
        self.new_user_window.destroy()


    #capturing the photo for the new user
    def add_img_to_label(self,label):
        imgtk = ImageTk.PhotoImage(image= self.recent_captured_pil)
        label.imgtk = imgtk
        label.configure(image = imgtk)

        self.new_user_photo = self.recent_captured_arr.copy()

    def accept_new_user(self):
        name = self.new_user_name.get(1.0,"end-1c")

        # saving photo to the db path
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.new_user_photo)

        # successful register operation
        util.msg_box('Welcome to the family !',""" the New user registered Successfully 

                           ╱|、
                          (˚ˎ 。7  
                          |、˜〵          
                          じしˍ,)ノ
                                            """)
        self.new_user_window.destroy()

    
    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__" :
    app = App()
    app.start()