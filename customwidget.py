from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from cardgame import Card,Player

class PlayerFrame(Frame):
    def __init__(self, parent,player:Player):
        Frame.__init__(self, parent)
        self.parent = parent
        self.player = player
        self.config(width=800,height=290,bg="green")
        self.pack(pady=10)
        self.pack_propagate(False)
        self.title_label = Label(self,text=self.player.name,font=("courier", 15),bg="green")
        self.title_label.pack(pady=5)      
        self.card_frame=Frame(self,width=800,height=240,bd=0,bg="green")
        self.card_frame.pack()
               
    def create_cardimg_label(self,card:Card,flag:bool=True):
        card_img = ImageTk.PhotoImage(self.resize_cards(card))
        self.player.cards_img[card.symbol] = card_img
        if not card.show:
            card_back_img=Image.open("cards/cardback.png")
            card_back_img=card_back_img.resize((150,218))
            card_img = ImageTk.PhotoImage(card_back_img)
            self.player.cards_img["card"] = card_img
            
        imglabel=Label(self.card_frame,image=card_img,bg="green")
        imglabel.pack(padx=3,side=LEFT)
        if not card.show and flag:
            imglabel.bind("<Button-1>",lambda event,card=card:self.display_card(card))
        self.player.cards_labels.append(imglabel) 
               
    def resize_cards(self,card:Card):
        filename=f"cards/{card.img_name}"
        card_img=Image.open(filename)
        card_resize_img=card_img.resize((150,218))  
        return card_resize_img 
       
    def display_card(self,card:Card):
        if card.show:
            
            self.player.cards_labels[0].config(image=self.player.cards_img["card"])
            card.show=False
        else:
            key=card.symbol
            self.player.cards_labels[0].config(image=self.player.cards_img[key])
            card.show=True
    
    def clear_cardframe(self):
        for widget in self.card_frame.winfo_children():
             widget.destroy()
             
    def sort_imglabel(self):
        player_sortedcards=self.player.sortedcards()
        for label in self.player.cards_labels:
            key=player_sortedcards[0].symbol
            label.config(image=self.player.cards_img[key])
            player_sortedcards.pop(0)
            
if __name__ == "__main__":
    root=Tk()
    board=PlayerFrame(root,"Computer")
    root.mainloop()
      
        