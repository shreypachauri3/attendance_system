import tkinter as tk
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from tkinter import messagebox
from tkinter import filedialog
import subprocess
# from attendance import TakeImages as TakeImages
# from attendance import TrainImages as TrainImages




# Create the root window
root = tk.Tk()
root.title("Feed Data")
root.overrideredirect(True)

def browse_file():
    file_path = filedialog.askopenfilename()
    return file_path

def run_jj():
    root.destroy()
    os.system('python jj.py')


# Set the window size and position
width = 700
height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width/2) - (width/2))
y = int((screen_height/2) - (height/2))

root.geometry(f"{width}x{height}+{x}+{y}")

x_cord = 75;
y_cord = 20;
checker=0;


# Set the background color to white
root.configure(bg="white")

# Add logo to the top left corner
logo_img = tk.PhotoImage(file="logo.png")
logo_img = logo_img.subsample(1)

# Create a label widget for the logo and pack it in the top left corner
logo_label = tk.Label(root, image=logo_img, bd=0)
logo_label.pack(side="left", anchor="nw", padx=10, pady=10)



# Add text to the right of the logo
text_label= tk.Label(root, text="ATTENDANCE MANAGEMENT PORTAL" ,bg="white"  ,fg="black"  ,width=35  ,height=1,font=('Sitka Text Semibold', 18, 'bold underline')) 

text_label.pack(pady=30, anchor="n")

line_canvas = tk.Canvas(root, height=1, width = 700,bg="black", highlightthickness=0)
line_canvas.create_line(0, 0, width, 0, fill="black")
line_canvas.place(x=75-x_cord,y=120-y_cord)


button_image = tk.PhotoImage(file="back.png")

# Create a button with the image and white background
button = tk.Button(root, image=button_image, bd=0, highlightbackground="white",bg="white", highlightcolor="white", command=run_jj)


# Place the button in the bottom right corner
button.place(x=80-x_cord, y=125-y_cord)

message = tk.Label(root, text="Status:", width=5  ,height=1  ,fg="black"  ,bg="white" ,font=('Sitka Text Semibold', 18, ' bold ') ) 
message.place(x=120-x_cord, y=160-y_cord)
def clear1():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)  
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if not Id:
        res="Please enter Id"
        message.configure(text = res)
        MsgBox = tk.messagebox.askquestion ("Warning","Please enter roll number properly , press yes if you understood",icon = 'warning')
        if MsgBox == 'no':
            tk.messagebox.showinfo('Your need','Please go through the readme file properly')
    elif not name:
        res="Please enter Name"
        message.configure(text = res)
        MsgBox = tk.messagebox.askquestion ("Warning","Please enter your name properly , press yes if you understood",icon = 'warning')
        if MsgBox == 'no':
            tk.messagebox.showinfo('Your need','Please go through the readme file properly')
        
    elif(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)

def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    clear1();
    clear2();
    message.configure(text= res)
    tk.messagebox.showinfo('Completed','Your model has been trained successfully!!')

def getImagesAndLabels(path):

    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    
    faces=[]

    Ids=[]

    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

# # Add a line below the "Attendance list:" line
# line2_canvas = tk.Canvas(root, height=1, bg="black", highlightthickness=0)
# line2_canvas.create_line(0, 0, width, 0, fill="black")
# line2_canvas.place(x=120-x_cord, y=150-y_cord)

output_box = tk.Text(root, height=3, width=67, bg="#f0f4f9", fg="black", font=("Helvetica", 12), wrap="word", state="disabled")
output_box.place(x=120-x_cord, y=200-y_cord)


lbl = tk.Label(root, text="ENTER YOUR COLLEGE ID", width=21  ,height=1  ,fg="black"  ,bg="white" ,font=('Sitka Text Semibold', 15, ' bold ') ) 
lbl.place(x=120-x_cord, y=280-y_cord)


txt = tk.Entry(root,width=26,bg="blue" ,fg="white",font=('Times New Roman', 15, ' bold '))
txt.place(x=120-x_cord, y=318-y_cord)

lbl = tk.Label(root, text="ENTER YOUR NAME", width=16  ,height=1  ,fg="black"  ,bg="white" ,font=('Sitka Text Semibold', 15, ' bold ') ) 
lbl.place(x=466-x_cord, y=280-y_cord)

txt2 = tk.Entry(root,width=26  ,bg="blue"  ,fg="white",font=('Times New Roman', 15, ' bold ')  )
txt2.place(x=466-x_cord, y=318-y_cord)

button_font = ('Arial', 12, 'bold')


button = tk.Button(root, text="UPLOAD YOUR PICTURE", command=browse_file  ,width=21  ,height=1  ,fg="black"  ,bg="#f0f3f9" ,font=('Sitka Text Semibold', 15, ' bold '))
button.place(x=120-x_cord, y=380-y_cord)

takeImg = tk.Button(root, text="CAPTURE IMAGES", command=TakeImages  ,width=21  ,height=1  ,fg="black"  ,bg="#f0f3f9" ,font=('Sitka Text Semibold', 15, ' bold '))
takeImg.place(x=466-x_cord, y=380-y_cord)

trainImg = tk.Button(root, text="TRAIN MODEL", command=TrainImages  ,width=40 ,height=1  ,fg="black"  ,bg="#57a0e9" ,font=('Sitka Text Semibold', 18, ' bold ') )
trainImg.place(x=120-x_cord, y=460-y_cord)

exit_button = tk.Button(root, text="EXIT", width=10, height=1, bg="red", fg="white", font=('Sitka Text Semibold', 15, 'bold'), command=root.destroy)
exit_button.place(x=width-152, y=height-70)

# Run the main loop
root.mainloop()
