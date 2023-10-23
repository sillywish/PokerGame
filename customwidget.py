from tkinter import *
from tkinter import ttk

from dataclasses import dataclass

from PIL import Image, ImageTk
from cardgame import *
from copy import deepcopy
from cardgame import Card, Player

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
    # stock_width: int
    # stock_height: int
    
    
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
#DEFAULT_SIZE=percent(DEFAULT_SIZE,percent=0.8)
SM_SIZE=percent(DEFAULT_SIZE,percent=0.5)
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
        
    
    def create_card_back(self):
        card_back_img=Image.open("cards/cardback.png")
        card_back_img=card_back_img.resize(self.SIZE.card_size)
        card_img = ImageTk.PhotoImage(card_back_img)
        self.player.cards_img["card"] = card_img
        
    #使用pack()部署卡片图片使用于简单的游戏规则  
    def create_cardimg_label(self,card:Card,flag:bool=True):
        
        if "card" not in self.player.cards_img:
            self.create_card_back()
        if card.symbol not in self.player.cards_img:
            card_img = ImageTk.PhotoImage(self.resize_cards(card))
            self.player.cards_img[card.symbol] = card_img
        else:
            card_img = self.player.cards_img[card.symbol]
        # card_img = ImageTk.PhotoImage(self.resize_cards(card))
        # self.player.cards_img[card.symbol] = card_img
        if not card.show:
            card_img = self.player.cards_img["card"] 
            # card_back_img=Image.open("cards/cardback.png")
            # card_back_img=card_back_img.resize((150,218))
            # card_img = ImageTk.PhotoImage(card_back_img)
            # self.player.cards_img["card"] = card_img
            
        # imglabel=Label(self.card_frame,image=card_img,bg="green")
        position = len(self.player.cards)-1
        imglabel=CardLabel(self.card_frame,card=card,position=position,image=card_img,bg="green")
        imglabel.pack(padx=3,side=LEFT)
        if not card.show and flag:
            imglabel.bind("<Button-1>",lambda event : self._display_card(event))
        self.player.cards_labels.append(imglabel) 
    
    #使用place()部署卡片图片使用于复杂的游戏规则          
    def _create_cardimg_label(self,card:Card,flag:bool=True):
        """使用place()部署卡片图片使用于复杂的游戏规则 """
        
        if "card" not in self.player.cards_img:
            self.create_card_back()        
        #if img is not exsit then create one
        if card.symbol not in self.player.cards_img:
            card_img = ImageTk.PhotoImage(self.resize_cards(card))
            self.player.cards_img[card.symbol] = card_img
        else:
            card_img = self.player.cards_img[card.symbol]
        
        # create the back img      
        if not card.show:
            card_img = self.player.cards_img["card"] 
            
        position = len(self.player.cards)-1
        imglabel=CardLabel(self.card_frame,card=card,position=position,image=card_img,)
        
        #if flag is true add event when click img can flip over
        # if not card.show and flag:
        #     imglabel.bind("<Button-1>",lambda event : self._display_card(event))
        if card.show:
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
             
    def sort_imglabel(self,flag=True):
        """sorted player cards
        """
        if flag:
            self.player.sortedcards()
        else:
            self.player.sortedcards_by_num()
            
        player_sortedcards=deepcopy(self.player.cards)
        position=0
        for label in self.player.cards_labels:
            
            label.card=player_sortedcards[0]
            label.position=position
            position+=1
            if label.card.show:
                key=player_sortedcards[0].symbol
                label.config(image=self.player.cards_img[key])
            player_sortedcards.pop(0)
    
    def _add_card(self,card:Card,):
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
            label.destroy()
            index_remove_list.append(card_tuple[1])
            cards_list.append(card_tuple[0])

        #according to the index_remove_list delete relative obj of cards
        index_remove_list.sort(reverse=True)
        for index in index_remove_list:
            self.player.cards_labels.pop(index)
            self.player.cards.pop(index) 
        self.picked_cards.clear()
        self.sort_imglabel()
        self.reposition()
        return cards_list
        
    
    def destroy_card_by_index(self,index_list:list[int]) -> None:
        
        index_list.sort(reverse=True)
        for index in index_list:
            self.player.cards_labels[index].destroy()
            self.player.cards_labels.pop(index)
            self.player.cards.pop(index)
                   
    def get_picked_cards(self) -> list[Card]:

        cards_list: list[Card] =[]
        
        #sotre the index of picked cards
        for label, card_tuple in self.picked_cards.items():
            cards_list.append(card_tuple[0])
        return cards_list

# class RummyDeck(Deck):
    
#     def __init__(self) -> None:
#         super().__init__()
#         self.cards_img:dict={}
#         self.img_labels : list[CardLabel]=[]
#         #self.discard_label : list[CardLabel]=[]

class DeckFrame(Frame):
    
    def __init__(self, parent,update_state,size=DEFAULT_SIZE):
        Frame.__init__(self, parent)
        self.parent = parent
        self.deck = RummyDeck()
        self.state = RummyGameState.DRAWCARD
        self.SIZE = size
        self.update_state = update_state
        self.picked_cards=[]
        self.topcard_position=None
        self.config(width=self.SIZE.frame_width,
                    height=self.SIZE.frame_height,
                    bg=self.SIZE.frame_bg,)
        # self.pack(pady=10)
        self.pack_propagate(False)
        self.stock = Frame(self,width=self.SIZE.frame_width/2,height=self.SIZE.frame_height,bg="red")
        self.stock.pack(side=LEFT)
        self.discard_pile = Frame(self,width=self.SIZE.frame_width/2,height=self.SIZE.frame_height,bg="black")
        self.discard_pile.pack(side=LEFT)
    
    def create_deck(self) -> None:
        """according self.deck create imglabel"""      
        
        for card in self.deck.cards[:-1]:
            self.create_cardimg_label(card)
        self.create_discard_label(self.deck.cards[-1])
            
    def create_card_back(self):
        card_back_img=Image.open("cards/cardback.png")
        card_back_img=card_back_img.resize(self.SIZE.card_size)
        card_img = ImageTk.PhotoImage(card_back_img)
        self.deck.cards_img["card"] = card_img
                  
    def resize_cards(self,card:Card):
        filename=f"cards/{card.img_name}"
        card_img=Image.open(filename)
        #card_resize_img=card_img.resize((150,218))
        card_resize_img=card_img.resize(self.SIZE.card_size) 
        return card_resize_img     
    
    def create_cardimg_label(self, card: Card):
        """create card label obj for stock"""
        if "card" not in self.deck.cards_img:
            self.create_card_back()              
        card_img = self.deck.cards_img["card"]
           
        position = len(self.deck.img_labels)
        self.topcard_position = position
        imglabel=CardLabel(self.stock,card=card,position=position,image=card_img,)
        x_piont = -int(self.SIZE.card_size[0]/2)
        imglabel.place(x=x_piont,y=30,relx=0.5)
        
        #if flag is true add event when click img can flip over
        # if not card.show and flag:
        #     imglabel.bind("<Button-1>",lambda event : self._display_card(event))
        imglabel.bind("<Button-1>",lambda event : self.deal_card(event))
        self.deck.img_labels.append(imglabel)
     
    def create_discard_label(self,card:Card):
        """create card label obj for discard"""
        #if img is not exsit then create one
        if card.symbol not in self.deck.cards_img:
            card_img = ImageTk.PhotoImage(self.resize_cards(card))
            self.deck.cards_img[card.symbol] = card_img
        else:
            card_img = self.deck.cards_img[card.symbol]
            
        position = len(self.deck.img_labels)
        imglabel=CardLabel(self.discard_pile,card=card,position=position,image=card_img,)
        imglabel.place(x=-75,y=30,relx=0.5)
        imglabel.bind("<Button-1>",lambda event : self.deal_card(event))
        self.deck.img_labels.append(imglabel)
          
                
    def deal_card(self,event) -> None:
        """deal card funtion for click event"""
        widget = event.widget
        #print(widget)
        print(f"抽的卡的位置是{widget.position}")
        print(self.deck)
        print(f"抽牌堆最上面的卡的位置是{self.topcard_position}")
        #print(widget.card)
        position = widget.position
        #如果是从牌堆抽牌 记录的牌堆最上面的位置-1
        
        if self.state !=RummyGameState.DRAWCARD:
            return
        
        if self.topcard_position == position:
            self.topcard_position -=1
            
        

                
            
            
        #print(self.deck.img_labels)
        card=self.deck.cards.pop(position)
        for label in self.deck.img_labels[position:]:
            label.position-=1
        self.deck.img_labels.pop(position)
        #print(len(self.stock.children))
        #print(len(player.cards_labels))
        
        widget.destroy()
        print(card)
        
        #if topcard position<0 stock is empty so add discard to stock
        self.shuffle_discard_to_stock()
        
        state=RummyGameState.PLAYING
        self.update_state(state,card=card)
        self.state = state    
    
    
    def shuffle_discard_to_stock(self):
        if self.topcard_position >=0:
            return
        for widget in self.discard_pile.winfo_children():
             widget.destroy()
        self.deck.img_labels.clear()
        last_card=self.deck.cards[-1]
        self.deck.cards=self.deck.cards[:-1]
        self.deck.shuffle()
        self.deck.cards = self.deck.cards+[last_card]
        self.create_deck()
        
    
    def _deal_card(self) -> Card:
        """deal card from stock"""
        widget = self.deck.img_labels[self.topcard_position]
        print(f"抽的卡的位置是{widget.position}")
        print(self.deck)
        print(f"抽牌堆最上面的卡的位置是{self.topcard_position}")
        card=self.deck.cards.pop(self.topcard_position)
        for label in self.deck.img_labels[self.topcard_position:]:
            label.position-=1
        self.deck.img_labels.pop(self.topcard_position)
        self.topcard_position-=1
        #print(len(self.stock.children))
        #print(len(player.cards_labels))        
        widget.destroy()
        self.shuffle_discard_to_stock()
        return card
    
    def _deal_card_from_discard(self) -> Card:
        """deal card from discard"""
        widget = self.deck.img_labels[-1]
        position = widget.position
        print(f"抽的卡的位置是{position}")
        print(self.deck)
        print(f"抽牌堆最上面的卡的位置是{len(self.deck.img_labels)}")
        card=self.deck.cards.pop(position)
        for label in self.deck.img_labels[position:]:
            label.position-=1
        self.deck.img_labels.pop(position)     
        widget.destroy() 
        return card
    
    def pass_to_discard(self,card:Card):
        self.create_cardimg_label
              
if __name__ == "__main__":
    root=Tk()
    player=Player("Computer")
    board=DeckFrame(root,None)
    playerboard=PlayerFrame(root,player)
    for _ in range(10):
        playerboard._add_card(board.deck.deal())
    # board=PlayerFrame(root,player,size=SM_SIZE)
    # for _ in range(4):
    #     board.player.cards.append(random_generate_card())
    board.create_deck()
    # print(board.SIZE)
    #print(player.cards_labels)
    root.mainloop()

        