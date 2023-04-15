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

# Create the root window
root = tk.Tk()
root.title("Attendance Management Portal")

root.overrideredirect(True)


# Set the window size and position
width = 700
height = root.winfo_screenheight()-100 # Get the screen height
# Calculate the x- and y-coordinates to center the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width/2) - (width/2))
y = int((screen_height/2) - (height/2))

root.geometry(f"{width}x{height}+{x}+{y}")

x_cord = 75;
y_cord = 20;
checker=0;


message2 = tk.Text(root, height=screen_height*0.025, width=67, bg="#f0f4f9", fg="black", font=("Helvetica", 12), wrap="word", state="disabled")
message2.place(x=120-x_cord, y=290-y_cord)

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    res=attendance
    message2.configure(text= res)
    res = "Attendance Taken"
    # message.configure(text= res)
    # tk.messagebox.showinfo('Completed','Congratulations ! Your attendance has been marked successfully for the day!!')

    


# Set the background color to white
root.configure(bg="white")

# Add logo to the top left corner
logo_img = tk.PhotoImage(file="logo.png")
logo_img = logo_img.subsample(1)

def run_jjcopy():
    root.destroy()
    os.system('python jjcopy.py')

# Create a label widget for the logo and pack it in the top left corner
logo_label = tk.Label(root, image=logo_img, bd=0)
logo_label.pack(side="left", anchor="nw", padx=10, pady=10)



# Add text to the right of the logo
text_label= tk.Label(root, text="ATTENDANCE MANAGEMENT PORTAL" ,bg="white"  ,fg="black"  ,width=35  ,height=1,font=('Sitka Text Semibold', 18, 'bold underline')) 

text_label.pack(pady=30, anchor="n")

line_canvas = tk.Canvas(root, height=1, width = 700,bg="black", highlightthickness=0)
line_canvas.create_line(0, 0, width, 0, fill="black")
line_canvas.place(x=75-x_cord,y=120-y_cord)










trackImg = tk.Button(root, text="MARK ATTENDANCE", command=TrackImages, width=40 ,height=1  ,fg="black"  ,bg="#57a0e9" ,font=('Sitka Text Semibold', 18, ' bold ') )
trackImg.place(x=120-x_cord, y=150-y_cord)


lbl = tk.Label(root, text="Attendance list:", width=12  ,height=1  ,fg="black"  ,bg="white" ,font=('Sitka Text Semibold', 18, ' bold ') ) 
lbl.place(x=120-x_cord, y=250-y_cord)


# # Add a line below the "Attendance list:" line
# line2_canvas = tk.Canvas(root, height=1, bg="black", highlightthickness=0)
# line2_canvas.create_line(0, 0, width, 0, fill="black")
# line2_canvas.place(x=120-x_cord, y=150-y_cord)




button_image = tk.PhotoImage(file="button.png")

# Create a button with the image and white background
button = tk.Button(root, image=button_image, bd=0, highlightbackground="white",bg="white", highlightcolor="white",command=run_jjcopy)

# Place the button in the bottom right corner
button.place(x=width-70, y=height-70)

# Add an exit button in the bottom left corner
exit_button = tk.Button(root, text="EXIT", width=10, height=1, bg="red", fg="white", font=('Sitka Text Semibold', 15, 'bold'), command=root.destroy)
exit_button.place(x=20, y=height-70)



# Run the main loop
root.mainloop()
