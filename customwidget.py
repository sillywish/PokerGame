from tkinter import *
from tkinter import ttk

from enum import Enum,auto
from PIL import Image, ImageTk
from cardgame import Card,Player,random_generate_card

class PlayerFrame(Frame):
    def __init__(self, parent,player:Player):
        Frame.__init__(self, parent)
        self.parent = parent
        self.player = player
        self.picked_cards={}
        self.config(width=800,height=290,bg="green")
        self.pack(pady=10)
        self.pack_propagate(False)
        self.title_label = Label(self,text=self.player.name,font=("courier", 15),bg="green")
        self.title_label.pack(pady=5)      
        self.card_frame=Frame(self,width=800,height=240,bd=0,bg="red")
        self.card_frame.pack()
    
    #使用pack()部署卡片图片使用于简单的游戏规则  
    def create_cardimg_label(self,card:Card,flag:bool=True):
        card_img = ImageTk.PhotoImage(self.resize_cards(card))
        self.player.cards_img[card.symbol] = card_img
        if not card.show:
            card_back_img=Image.open("cards/cardback.png")
            card_back_img=card_back_img.resize((150,218))
            card_img = ImageTk.PhotoImage(card_back_img)
            self.player.cards_img["card"] = card_img
            
        # imglabel=Label(self.card_frame,image=card_img,bg="green")
        imglabel=CardLabel(self.card_frame,card=card,image=card_img,bg="green")
        imglabel.pack(padx=3,side=LEFT)
        if not card.show and flag:
            imglabel.bind("<Button-1>",lambda event : self._display_card(event))
        self.player.cards_labels.append(imglabel) 
    
    #使用place()部署卡片图片使用于复杂的游戏规则          
    def _create_cardimg_label(self,card:Card,flag:bool=True):
        
        #if img is not exsit then create one
        if card.symbol not in self.player.cards_img:
            card_img = ImageTk.PhotoImage(self.resize_cards(card))
            self.player.cards_img[card.symbol] = card_img
        else:
            card_img = self.player.cards_img[card.symbol]
        
        # create the back img      
        if not card.show:
            card_back_img=Image.open("cards/cardback.png")
            card_back_img=card_back_img.resize((150,218))
            card_img = ImageTk.PhotoImage(card_back_img)
            self.player.cards_img["card"] = card_img
        imglabel=CardLabel(self.card_frame,card=card,image=card_img,)
        
        #if flag is true add event when click img can flip over
        if not card.show and flag:
            imglabel.bind("<Button-1>",lambda event : self._display_card(event))
        imglabel.bind("<Button-1>",lambda event : self.get_card_obj(event))
        self.player.cards_labels.append(imglabel)        
        self.reposition()
               
    def resize_cards(self,card:Card):
        filename=f"cards/{card.img_name}"
        card_img=Image.open(filename)
        card_resize_img=card_img.resize((150,218))  
        return card_resize_img 
      
    def get_card_obj(self,event):
        card_obj=event.widget
        #print(card_obj.card)
        if card_obj.state == CardState.NORMAL:
            card_obj.place(rely=0.05)
            card_obj.state = CardState.PICK
            self.picked_cards[card_obj]=card_obj.card
        elif card_obj.state == CardState.PICK:
            card_obj.place(rely=0.1)
            card_obj.state = CardState.NORMAL
            self.picked_cards.pop(card_obj)
      
    def _display_card(self,event):
        
        label_obj = event.widget
        card=label_obj.card
        if card.show:
            
            label_obj.config(image=self.player.cards_img["card"])
            card.show=False
        else:
            key=card.symbol
            label_obj.config(image=self.player.cards_img[key])
            card.show=True
            
            
    def display_card(self,card: Card):
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
            label.card=player_sortedcards[0]
            label.config(image=self.player.cards_img[key])

            player_sortedcards.pop(0)
    
    #使用()部署创建卡片图片使用于复杂的游戏规则
    def _add_card(self,card:Card):
        self.player.cards.append(card)
        self._create_cardimg_label(card)
    
    #使用()部署创建卡片图片使用于简单的游戏规则    
    def add_card(self,card:Card):  
        self.player.cards.append(card)
        self.create_cardimg_label(card)
        
    def reposition(self) -> None:
        num_cards = len(self.player.cards)-1
        startpoint = int(-(num_cards*30+150)/2)
        for label in self.player.cards_labels:
            label.place_forget()
            label.place(x=startpoint,relx=0.5,rely=0.1)
            startpoint+=30   


class CardLabel(Label):
    def __init__(self,parent,card,*args, **kwargs):
        Label.__init__(self,parent,*args, **kwargs)
        self.state: CardState = CardState.NORMAL
        self.card: Card =card
        
   
class CardState(Enum):
    NORMAL = auto()
    PICK = auto()            
            
if __name__ == "__main__":
    root=Tk()
    player=Player("Computer")

    
    board=PlayerFrame(root,player)
    for _ in range(10):
        board._add_card(random_generate_card())
    board.sort_imglabel()
    print(player.cards_labels)
    root.mainloop()
      
        