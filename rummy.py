from tkinter import *
from tkinter import ttk,messagebox
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
        self.meld_list: list[PlayerFrame]=[]
        #self.display=Player("display")
        
        
        
        computer_frame = PlayerFrame(self,self.computer)
        computer_frame.grid(row=0)
        self.frame_list['computer_frame']=computer_frame
        
        stock =DeckFrame(self,self.update_state)
        stock.grid(row=1,column=0)
        self.frame_list['stock_frame']=stock
        
        meld_frame = Frame(self,width=DEFAULT_SIZE.frame_width/2,height=DEFAULT_SIZE.frame_height*3,bg="blue")
        meld_frame.grid(row=0,column=1,rowspan=3)
        meld_frame.pack_propagate(False)
        self.frame_list['meld_frame']=meld_frame
    
        player_frame=PlayerFrame(self,self.player)
        player_frame.grid(row=2,)
        self.frame_list['player_frame']=player_frame
        
        button_frame = Frame(self,width=DEFAULT_SIZE.frame_width,height=50)
        button_frame.grid(row=3,column=0)
        #stock.current_player=player_frame 
        stock.deck.shuffle()
        
        for _ in range(10):
            card=stock.deck.deal()
            card.show=False
            computer_frame._add_card(card)
            player_frame._add_card(stock.deck.deal())
        computer_frame.sort_imglabel()    
        player_frame.sort_imglabel()
        stock.create_deck()
        # for _ in range(10):
        #     self.board._add_card(random_generate_card())
        # self.board.sort_imglabel()
        self.meld_button=Button(button_frame,text="meld",command=self.play_cards)
        self.meld_button.pack(side=LEFT)
        self.layout_button=Button(button_frame,text="layout",command=self.layout)
        self.layout_button.pack(side=LEFT)
        self.button=Button(button_frame,text="discard",command=self.discard)
        self.button.pack(side=LEFT)

    
    def discard(self):
        played_card: list[Card]=self.frame_list['player_frame'].destroy_picked_cards()
        for card in played_card:
             self.frame_list['stock_frame'].create_discard_label(card)
             self.frame_list['stock_frame'].deck.cards.append(card)
        if not self.check_goout():
            self.computer_moves()
            self.update_state(RummyGameState.DRAWCARD)

    def play_cards(self):
        played_card = self.frame_list['player_frame'].get_picked_cards()
        print(played_card)
        if not rummy_is_run(played_card) and not rummy_is_set(played_card):
            print("无效的卡牌组合")
            return
        
        played_card = self.frame_list['player_frame'].destroy_picked_cards()
        self.create_setframe(played_card)
        if not self.check_goout():
            self.update_state(RummyGameState.DISCARD)
    
    def layout(self):
        layout_cards :list[tuple[list[Card],PlayerFrame]]= []
        for frame in self.meld_list:
            layout_cards.append((find_layout_cards(frame.player.cards),frame))
         
        print(layout_cards)       
        played_card = self.frame_list['player_frame'].get_picked_cards()[0]
        
        print(self.frame_list['player_frame'].player.cards.index(played_card))
        del_index = None
        is_vaild = False
        for index,item in enumerate(layout_cards):
            if played_card in item[0]:
                played_card = self.frame_list['player_frame'].destroy_picked_cards()[0]
                item[1]._add_card(played_card)
                item[1].sort_imglabel()
                is_vaild = True
                if find_layout_cards(item[1].player.cards) is None:
                    del_index = index
            
        if not is_vaild:
            print("you can,t lay out")
        if del_index is not None:
            self.meld_list.pop(del_index)
        
        self.check_goout()
            
    
    def check_goout(self) -> bool:
        if  len(self.frame_list['player_frame'].player.cards) == 0 or len(self.frame_list['computer_frame'].player.cards) == 0:
            self.update_state(RummyGameState.GOOUT)
            return True
        return False
    
    def show_winner(self) -> None:
        if len(self.frame_list['player_frame'].player.cards) == 0:
            messagebox.showinfo("showinfo", "winner is player") 
            
        else:
            messagebox.showinfo("showinfo", "winner is computer") 
            
        
    
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
        elif state == RummyGameState.GOOUT:
            self.frame_list['stock_frame'].state =RummyGameState.GOOUT
            self.state = RummyGameState.GOOUT
            self.show_winner()

            
        #self.board.picked_cards.clear()
        # for card in played_card:
        #     self.displsyboard._add_card(card)
            
    def computer_moves(self):
        
        #deal_card
        card = None
        discard_card = self.frame_list["stock_frame"].deck.cards[-1]
        temp_cards=self.frame_list["computer_frame"].player.cards.copy()
        temp_cards.append(discard_card)
        print(temp_cards)
        deal_test = RummyAI(temp_cards)
        deal_test.cards=sorted(temp_cards,key=lambda x:x.num)
        if deal_test.has_run():
            card = self.frame_list["stock_frame"]._deal_card_from_discard()
        deal_test.cards=sorted(temp_cards,key=lambda x:x.value)
        if deal_test.has_set():
            card = self.frame_list["stock_frame"]._deal_card_from_discard()
        # print(id(self.frame_list["computer_frame"].player.cards))
        if card is None:
            print(f"抽的是抽牌堆")
            card = self.frame_list["stock_frame"]._deal_card()
        print(f"computer deal {card}")
        card.show=False
        self.frame_list["computer_frame"]._add_card(card)
        
        #COMPUTER Playing either meld or check can lay out
        test = RummyAI(self.frame_list["computer_frame"].player.cards)
        
        while test.has_set() or test.has_run():
            print(test.cards)
            print(self.frame_list["computer_frame"].player.cards)
            test.recalculate()
            if test.has_run():
                self.frame_list["computer_frame"].sort_imglabel(flag=False)
                self.computer_meld(test.has_run())
                if len(test.cards) ==0:
                    break
                
            elif test.has_set():
                self.frame_list["computer_frame"].sort_imglabel()
                
                self.computer_meld(test.has_set())
                if len(test.cards) ==0:
                    break
            
            
                
        #funtion for check if has card for lay out 
        if self.state == RummyGameState.GOOUT:
            return
        self.computer_layout()
        #discard()
        
        
        if self.state == RummyGameState.GOOUT:
            return
        
        self.computer_discard()
        
        self.check_goout()
    
    def computer_meld(self,indexlist):
        play_card = self.frame_list["computer_frame"].player.cards[indexlist[0]:indexlist[-1]+1]
        for card in play_card:
            card.show=True
        print(f"computer 有可以MELD的牌{play_card}")
        self.create_setframe(played_card=play_card)         
        self.frame_list["computer_frame"].destroy_card_by_index(indexlist)
        self.frame_list["computer_frame"].reposition()
        
        self.check_goout()
        
    def computer_layout(self):
        layout_cards :list[list[list[Card],PlayerFrame]]= []
        for frame in self.meld_list:
            layout_cards.append([find_layout_cards(frame.player.cards),frame])
        
        del_index = None
        new_layout = None
        index=0
        print(layout_cards)
        while index<len(layout_cards) and len(layout_cards)>0:
            for card in layout_cards[index][0]:
                if card in self.frame_list["computer_frame"].player.cards:
                    card_index=self.frame_list["computer_frame"].player.cards.index(card)
                    print(f"computer has {card} for lay out")
                    self.frame_list['computer_frame'].destroy_card_by_index([card_index])
                    self.frame_list["computer_frame"].reposition()
                    layout_cards[index][1]._add_card(card)
                    layout_cards[index][1].sort_imglabel()
                    new_layout=find_layout_cards(layout_cards[index][1].player.cards)
                    if new_layout is None:
                        del_index = index
                        print(f"delete index is {del_index}")
                    
                    index = 0
                    break
            if new_layout:
                layout_cards[index][0]=new_layout
            #!!! python 中 的 if 判断 0 也是False
            if del_index is not None:
                self.meld_list.pop(del_index)
                layout_cards.pop(del_index)
                print(self.meld_list)
                del_index = None
            else:
                index +=1
         
        self.check_goout() 
    
    def computer_discard(self):
        print(self.frame_list["computer_frame"].player.cards)
        cost_list = cal_cost_rummy(self.frame_list["computer_frame"].player.cards)
        print(cost_list)
        print(cost_list.index(min(cost_list)))
        
        discard_index = cost_list.index(min(cost_list))
        #discard_index = random.choice(self.frame_list["computer_frame"].player.cards_labels).position
        print(f"要丢弃的卡的位置是{discard_index}")
        
        discard=self.frame_list["computer_frame"].player.cards[discard_index]
        discard.show=True
        print(discard)
        self.frame_list['stock_frame'].create_discard_label(discard)
        self.frame_list['stock_frame'].deck.cards.append(discard)
        self.frame_list["computer_frame"].destroy_card_by_index([discard_index])
        self.frame_list["computer_frame"].reposition()
    
                                       
    def create_setframe(self,played_card):
        temp_set = Player()
        set_frame=PlayerFrame(self.frame_list['meld_frame'],temp_set,size=SM_SIZE)
        set_frame.title_label.pack_forget()
        set_frame.pack_propagate(True)
        for card in played_card:
            set_frame._add_card(card)
        set_frame.sort_imglabel()
        
        set_frame.pack()
        if len(played_card) == 4 and rummy_is_set(played_card):
            return
        self.meld_list.append(set_frame)   

        
if __name__ == "__main__":
    root=Tk()
    
    root.geometry("1200x1000")
    RummyGame(root).pack(side="top", fill="both", expand=True)

    root.mainloop()
      