from tkinter import *
from tkinter import ttk

from cardgame import *
from customwidget import PlayerFrame,SM_SIZE,DeckFrame

class BridgeGame(Frame):
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.parent = parent
        self.player=Player("Computer")
        #self.display=Player("display")
        self.stock =DeckFrame(self)
       
        
        #self.displsyboard=PlayerFrame(self,self.display,size=SM_SIZE)
        

    
        self.board=PlayerFrame(self,self.player)
        
        self.stock.current_player=self.board
        
        self.stock.deck.shuffle()
        
        for _ in range(10):
            self.board._add_card(self.stock.deck.deal())
        self.board.sort_imglabel()
        self.stock.create_deck()
        # for _ in range(10):
        #     self.board._add_card(random_generate_card())
        # self.board.sort_imglabel()
        self.button=Button(self,text="deal",command=self.play_cards)
        self.button.pack()
        self.button=Button(self,text="discard",command=self.discard)
        self.button.pack()

    
    def discard(self):
        played_card: list[Card]=self.board.destroy_picked_cards()
        for card in played_card:
            self.stock.create_discard_label(card)
            self.stock.deck.cards.append(card)

    def play_cards(self):
        card = self.stock._deal_card()
        print(card)
        self.board._add_card(card)
        
        #self.board.picked_cards.clear()
        # for card in played_card:
        #     self.displsyboard._add_card(card)
            
      
    
        # for laber in self.player.cards_labels:
        #     print(id(laber))    

        # print([id(item) for _,item in self.board.picked_cards.items()])
        
if __name__ == "__main__":
    root=Tk()
    
    root.geometry("1024x720")
    BridgeGame(root).pack(side="top", fill="both", expand=True)

    root.mainloop()
      