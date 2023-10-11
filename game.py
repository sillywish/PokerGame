from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Protocol
from cardgame import Card
from Blackjack import BlackJackGame
from Showhand import ShowHandGame



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

        label = Label(self, text="Poker Game",font=("courier", 40,"bold"),bg="green")
        label.pack(padx=10, pady=10,expand=True)

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        showhand_button = Button(
            self,
            text="Go to the Showhand",
            command=lambda: parent.show_frame(ShowHandGame),
            width=30,
        )
        showhand_button.pack(pady=20,)
        blackjack_button = Button(
            self,
            text="Go to the Blackjack",
            command=lambda: parent.show_frame(PageOne),
            width=30,
        )
        blackjack_button.pack(pady=20,expand=True)


class PageOne(BlackJackGame):
      
    def ui_initialize(self):
        super().ui_initialize()
        back_button=Button(self.widget_list["score_frame"], width=20,text="Back", command=lambda: self.parent.show_frame(MainPage))#button to close the window
        self.widget_list["back_button"]=back_button
        back_button.pack(pady=10,side=BOTTOM)     

    
if __name__ == "__main__":
    game= PokerGame()
    game.mainloop()
