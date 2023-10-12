from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Protocol
from cardgame import Card
from Blackjack import BlackJackGame
from Showhand import ShowHandGame
import customtkinter



class PokerGame(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Test Application")    
        self.geometry(f"1024x720")
        self.configure(background="green")
        
        self.frames={}
        for F in (MainPage,PageOne,ShowHandGame):
            frame=F(self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        #print(self.frames)
        self.show_frame(MainPage)
        
    def resize_cards(self,card:Card):
        filename=f"cards/{card.img_name}"
        card_img=Image.open(filename)
        card_resize_img=card_img.resize((150,218))  
        return card_resize_img

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()

class MainPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.config(width=1024,height=720,bg="green")

        title_frame=Canvas(self,bg="green",width=500,height=400,bd=0,highlightthickness=0)
        title_frame.pack(padx=10,pady=40,)
        button_frame=Frame(self,bg="green",width=500,height=240)
        button_frame.pack()
        button_frame.pack_propagate(False)
        
        card_img=Image.open("index.png")
        card_resize_img=card_img.resize((350,280))
        self.image = ImageTk.PhotoImage(card_resize_img)
        
        #title_frame.create_image(150, 150, image=self.image)  
        label = Label(title_frame, text="Poker Game",font=("courier", 40,"bold"),bg="green")
        label.pack(expand=True)
        title_label = Label(title_frame,image=self.image,bg="green")
        title_label.pack()
        
        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        showhand_button = Button(
            button_frame,
            text="Go to the Showhand",
            command=lambda: parent.show_frame(ShowHandGame),
            width=30,
        )
        showhand_button.pack(expand=True)
        blackjack_button = Button(
            button_frame,
            text="Go to the Blackjack",
            command=lambda: parent.show_frame(PageOne),
            width=30,
        )
        blackjack_button.pack(expand=True)


class PageOne(BlackJackGame):
      
    def ui_initialize(self):
        super().ui_initialize()
        back_button=Button(self.widget_list["score_frame"], width=20,text="Back", command=lambda: self.parent.show_frame(MainPage))#button to close the window
        self.widget_list["back_button"]=back_button
        back_button.pack(pady=10,side=BOTTOM)     

    
if __name__ == "__main__":
    game= PokerGame()
    game.mainloop()
