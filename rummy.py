from tkinter import *
from tkinter import ttk
from enum import Enum,auto
from cardgame import *
from customwidget import PlayerFrame,SM_SIZE,DeckFrame,DEFAULT_SIZE




class RummyGame(Frame):
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.parent = parent
        self.computer = Player("Computer")
        self.player=Player()
        self.state = RummyGameState.DRAWCARD
        self.frame_list: dict[str,PlayerFrame|DeckFrame]={}
        #self.display=Player("display")
        
        
        
        computer_frame = PlayerFrame(self,self.computer)
        computer_frame.grid(row=0)
        self.frame_list['computer_frame']=computer_frame
        
        stock =DeckFrame(self,self.update_state)
        stock.grid(row=1,column=0)
        self.frame_list['stock_frame']=stock
        
        meld_frame = Frame(self,width=DEFAULT_SIZE.frame_width/2,height=DEFAULT_SIZE.frame_height*2,bg="blue")
        meld_frame.grid(row=0,column=1,rowspan=2)
        self.frame_list['meld_frame']=meld_frame
    
        player_frame=PlayerFrame(self,self.player)
        player_frame.grid(row=2,)
        self.frame_list['player_frame']=player_frame
        
        #stock.current_player=player_frame 
        stock.deck.shuffle()
        
        for _ in range(10):
            card=stock.deck.deal()
            #card.show=False
            computer_frame._add_card(card)
            player_frame._add_card(stock.deck.deal())
        computer_frame.sort_imglabel()    
        player_frame.sort_imglabel()
        stock.create_deck()
        # for _ in range(10):
        #     self.board._add_card(random_generate_card())
        # self.board.sort_imglabel()
        self.meld_button=Button(self,text="meld",command=self.play_cards)
        self.meld_button.grid(row=3,column=0)
        self.button=Button(self,text="discard",command=self.discard)
        self.button.grid(row=2,column=1)

    
    def discard(self):
        played_card: list[Card]=self.frame_list['player_frame'].destroy_picked_cards()
        for card in played_card:
             self.frame_list['stock_frame'].create_discard_label(card)
             self.frame_list['stock_frame'].deck.cards.append(card)
        self.computer_moves()
        self.update_state(RummyGameState.DRAWCARD)

    def play_cards(self):
        played_card = self.frame_list['player_frame'].destroy_picked_cards()
        self.create_setframe(played_card)
        # temp_set = Player()
        # set_frame=PlayerFrame(self.frame_list['meld_frame'],temp_set,size=SM_SIZE)
        # for card in played_card:
        #     set_frame._add_card(card)
        # set_frame.pack()
        self.update_state(RummyGameState.DISCARD)
    
    
    def update_state(self,state:RummyGameState,card: Card | None =None) -> None:
        if state == RummyGameState.PLAYING:
            self.meld_button.config(state="normal")
            self.button.config(state="normal")
            self.frame_list['player_frame']._add_card(card)
            self.frame_list['player_frame'].sort_imglabel()
            self.state = RummyGameState.PLAYING 
        elif state == RummyGameState.DRAWCARD:
            self.frame_list['stock_frame'].state =RummyGameState.DRAWCARD
            self.state = RummyGameState.DRAWCARD
            self.meld_button.config(state="disabled")
            self.button.config(state="disabled")
        elif state == RummyGameState.DISCARD:
            self.frame_list['stock_frame'].state =RummyGameState.DISCARD
            self.state = RummyGameState.DISCARD
            self.button.config(state="normal")
            self.meld_button.config(state="disabled")
            
        #self.board.picked_cards.clear()
        # for card in played_card:
        #     self.displsyboard._add_card(card)
            
    def computer_moves(self):
        
        #deal_card
        card = self.frame_list["stock_frame"]._deal_card()
        print(f"computer deal {card}")
        self.frame_list["computer_frame"]._add_card(card)
        
        test = RummyAI(self.frame_list["computer_frame"].player.cards)
        
        self.frame_list["computer_frame"].sort_imglabel()
        res=test.has_set()
        if res:
            print(res)
            play_card = test.cards[res[0]:res[-1]+1]
            self.create_setframe(played_card=play_card)
            
            self.frame_list["computer_frame"].destroy_card_by_index(res)
            self.frame_list["computer_frame"].reposition()
            #self.frame_list["computer_frame"].destroy_card_by_index(res)
            
        self.frame_list["computer_frame"].sort_imglabel(flag=False)
        print(test.cards)
        res = test.has_run()
        if res:
            print(res)
            play_card = test.cards[res[0]:res[-1]+1]
            self.create_setframe(played_card=play_card)
            
            self.frame_list["computer_frame"].destroy_card_by_index(res)
            self.frame_list["computer_frame"].reposition()
        #funtion for cal what to do 
        
        
        #discard()
    def create_setframe(self,played_card):
        temp_set = Player()
        set_frame=PlayerFrame(self.frame_list['meld_frame'],temp_set,size=SM_SIZE)
        for card in played_card:
            set_frame._add_card(card)
        set_frame.pack()   

        
if __name__ == "__main__":
    root=Tk()
    
    root.geometry("1200x1000")
    RummyGame(root).pack(side="top", fill="both", expand=True)

    root.mainloop()
      