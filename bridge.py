from tkinter import *
from tkinter import ttk

from cardgame import *
from customwidget import PlayerFrame,SM_SIZE

class BridgeGame(Frame):
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.parent = parent
        self.player=Player("Computer")
        self.display=Player("display")
        
        self.displsyboard=PlayerFrame(self,self.display,size=SM_SIZE)
        print(self.displsyboard.SIZE)

    
        self.board=PlayerFrame(self,self.player)
        print(self.board.SIZE)
        for _ in range(10):
            self.board._add_card(random_generate_card())
        self.board.sort_imglabel()
        self.button=Button(self,text="pick",command=self.play_cards)
        self.button.pack()


    def play_cards(self):
        
        #self.board.picked_cards.clear()
        played_card: list[Card]=self.board.destroy_picked_cards()
        for card in played_card:
            self.displsyboard._add_card(card)
            
      
    
        # for laber in self.player.cards_labels:
        #     print(id(laber))    

        # print([id(item) for _,item in self.board.picked_cards.items()])
        
if __name__ == "__main__":
    root=Tk()
    
    root.geometry("1024x720")
    BridgeGame(root).pack(side="top", fill="both", expand=True)

    root.mainloop()
      