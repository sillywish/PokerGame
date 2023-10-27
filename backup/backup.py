
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
root = Tk()
# Create a photoimage object of the image in the path
root.geometry("1080x620")
s = ttk.Style()
s.configure('My.TFrame', background='red')
frame = Frame(width=800, height=20)


image1 = Image.open("cards/11_of_clubs.png")
width, height = image1.size
#print(width)
#print(height)

image1=image1.resize((150,218))
test = ImageTk.PhotoImage(image1)
label1 = Label(image=test)

imglist=[]
#Define function to hide the widget
def hide_widget(widget:Widget):
   widget.pack_forget()

#Define a function to show the widget
def show_widget(widget:Widget):
   widget.pack()  
   
def hello():
   image1 = Image.open("cards/11_of_clubs.png")
      

   image1=image1.resize((150,218))
   global label2,test
   
   test = ImageTk.PhotoImage(image1)
   imglist.append(test)
   
   
   label2 = Label(image=test)
   label2.pack(side=LEFT)
   # print("??")


hide_button = Button(frame,text="hide",command=lambda:hide_widget(label1))
hide_button.pack(side="left")
#hide_button.pack()
show_button = Button(frame,text="show",command=lambda:show_widget(label1))
show_button.pack(padx=10,pady=10,side="left")
add_button = Button(frame,text="add",command=hello)
add_button.pack(padx=10,pady=10,side="left")
#show_button.pack()

for i in imglist:
   global label
   label=Label(image=i)
   label.pack()
   

frame.pack(side="bottom",fill=None)

# Position image
root.mainloop()