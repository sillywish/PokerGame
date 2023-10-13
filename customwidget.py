from tkinter import *
from tkinter import ttk

from dataclasses import dataclass
from enum import Enum,auto
from PIL import Image, ImageTk
from cardgame import *
from copy import deepcopy

@dataclass
class FrameSize:
    frame_width: int 
    frame_height: int
    frame_bg: str
    card_frame_width: int
    card_frame_height: int
    card_frame_bg: str
    card_size: tuple[int,int]
    card_gap: int
    card_top_gap: int
    title_font: tuple
    
def percent(default:FrameSize,percent) ->FrameSize:
    frame_width = percent * default.frame_width
    frame_height = percent * default.frame_height
    card_frame_width = percent * default.card_frame_width
    card_frame_height = percent * default.card_frame_height
    card_size = tuple([int(i*percent) for i in default.card_size])
    card_gap = percent * default.card_gap
    card_top_gap = percent * default.card_top_gap
    frame_bg = default.frame_bg
    card_frame_bg = default.card_frame_bg
    title_font = (default.title_font[0], int(default.title_font[1]*percent))
    
    return FrameSize(
        frame_width = frame_width,
        frame_height = frame_height,
        frame_bg = frame_bg,
        card_frame_width = card_frame_width,
        card_frame_height = card_frame_height,
        card_frame_bg = card_frame_bg,
        card_size = card_size,
        card_gap = card_gap,
        card_top_gap = card_top_gap,
        title_font = title_font                
    )
    
DEFAULT_SIZE=FrameSize(
        frame_width = 800,
        frame_height = 300,
        frame_bg = "green",
        card_frame_width = 800,
        card_frame_height = 260,
        card_frame_bg = "green",
        card_size = (150,218),
        card_gap = 30,
        card_top_gap = 20, 
        title_font = ("courier", 15)      
    )
SM_SIZE=percent(DEFAULT_SIZE,percent=0.8)
BG_SIZE=percent(DEFAULT_SIZE,percent=1.4)

class PlayerFrame(Frame):
    def __init__(self, parent,player:Player,size=DEFAULT_SIZE):
        Frame.__init__(self, parent)
        self.parent = parent
        self.player = player
        self.SIZE = size
        self.picked_cards={}
        self.config(width=self.SIZE.frame_width,
                    height=self.SIZE.frame_height,
                    bg=self.SIZE.frame_bg,)
        #self.config(width=800,height=290,bg="green")
        self.pack(pady=10)
        self.pack_propagate(False)
        self.title_label = Label(self,text=self.player.name,font=self.SIZE.title_font,bg="green")
        self.title_label.pack(pady=5)
        self.card_frame=Frame(self,
                              width=self.SIZE.card_frame_width,
                              height=self.SIZE.frame_height,
                              bg=self.SIZE.card_frame_bg,
                              bd=0,)      
        #self.card_frame=Frame(self,width=800,height=240,bd=0,bg="red")
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
        position = len(self.player.cards)-1
        imglabel=CardLabel(self.card_frame,card=card,position=position,image=card_img,bg="green")
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
            
        position = len(self.player.cards)-1
        imglabel=CardLabel(self.card_frame,card=card,position=position,image=card_img,)
        
        #if flag is true add event when click img can flip over
        if not card.show and flag:
            imglabel.bind("<Button-1>",lambda event : self._display_card(event))
        imglabel.bind("<Button-1>",lambda event : self.get_card_obj(event))
        self.player.cards_labels.append(imglabel)        
        self.reposition()
               
    def resize_cards(self,card:Card):
        filename=f"cards/{card.img_name}"
        card_img=Image.open(filename)
        #card_resize_img=card_img.resize((150,218))
        card_resize_img=card_img.resize(self.SIZE.card_size) 
        return card_resize_img 
      
    def get_card_obj(self,event):
        card_obj=event.widget
        if card_obj.state == CardState.NORMAL:
            card_obj.place(y=int(self.SIZE.card_top_gap/2))
            card_obj.state = CardState.PICK
            self.picked_cards[card_obj]=(card_obj.card,card_obj.position)
        elif card_obj.state == CardState.PICK:
            card_obj.place(y=self.SIZE.card_top_gap)
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
        """sorted player cards
        """
        self.player.sortedcards()
        player_sortedcards=deepcopy(self.player.cards)
        position=0
        for label in self.player.cards_labels:
            key=player_sortedcards[0].symbol
            label.card=player_sortedcards[0]
            label.position=position
            position+=1
            label.config(image=self.player.cards_img[key])
            player_sortedcards.pop(0)
    

    def _add_card(self,card:Card):
        """
        add card for complex rule game
        """ 
        self.player.cards.append(card)
        self._create_cardimg_label(card)
    
      
    def add_card(self,card:Card):
        """
        add card for easy rule game  
        """  
        self.player.cards.append(card)
        self.create_cardimg_label(card)

        
    def reposition(self) -> None:
        """
        repositon card imglabel and adjust Cardlabel.postion
        """
        num_cards = len(self.player.cards)-1
        #startpoint = int(-(num_cards*30+150)/2)
        startpoint = int(-(num_cards*self.SIZE.card_gap+self.SIZE.card_size[0])/2)
        position=0
        for label in self.player.cards_labels:
            label.place_forget()
            label.place(x=startpoint,relx=0.5,y=self.SIZE.card_top_gap)
            label.position=position
            position+=1
            #startpoint+=30
            startpoint+=self.SIZE.card_gap  

    def destroy_picked_cards(self) -> list[Card]:
        """
        destory imglabel by picked_card
        and remove relative object of cards
        """
        #destroy_cards_list
        cards_list: list[Card] =[]
        
        #sotre the index of picked cards
        index_remove_list=[]
        for label, card_tuple in self.picked_cards.items():
            print(card_tuple)
            label.destroy()
            index_remove_list.append(card_tuple[1])
            cards_list.append(card_tuple[0])

        #according to the index_remove_list delete relative obj of cards
        index_remove_list.sort(reverse=True)
        for index in index_remove_list:
            self.player.cards_labels.pop(index)
            self.player.cards.pop(index) 
        self.picked_cards.clear()
        
        
        print(self.player.cards)

        
        
        #after remove cards repositon all remain cards
        self.reposition()
        
        print(cards_list)
        return cards_list
          
            
if __name__ == "__main__":
    root=Tk()
    player=Player("Computer") 
    board=PlayerFrame(root,player,size=SM_SIZE)
    for _ in range(10):
        board._add_card(random_generate_card())
    board.sort_imglabel()
    
    print(board.SIZE)
    #print(player.cards_labels)
    root.mainloop()

      
        