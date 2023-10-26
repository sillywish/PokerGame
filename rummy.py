#from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as st 
from tkinter import ttk,messagebox
from enum import Enum,auto
from cardgame import *
from customwidget import PlayerFrame,SM_SIZE,DeckFrame,DEFAULT_SIZE,MELD_SIZE,center
from usefulwidget import AutoScrollbarApp,ScrollbarApp




class RummyGame(tk.Frame):
    def __init__(self, parent,*args, **kwargs):
        tk.Frame.__init__(self, parent,*args, **kwargs)
        self.parent = parent
        self.computer = Player("Computer")
        self.player=Player()
        self.state = RummyGameState.DRAWCARD
        self.frame_list: dict[str,PlayerFrame|DeckFrame|AutoScrollbarApp]={}
        self.meld_list: list[PlayerFrame]=[]
        #self.display=Player("display")
        
        
        
        computer_frame = PlayerFrame(self,self.computer)
        computer_frame.grid(row=0,column=0)
        self.frame_list['computer_frame']=computer_frame
        
        stock =DeckFrame(self,self.update_state)
        stock.grid(row=1,column=0)
        self.frame_list['stock_frame']=stock
        
        # meld_frame = Frame(self,width=DEFAULT_SIZE.frame_width/2,height=DEFAULT_SIZE.frame_height*2,bg="blue")
        # meld_frame.grid(row=0,column=1,rowspan=2)
        # meld_frame.pack_propagate(False)
        
        meld_frame = ScrollbarApp(self,width=DEFAULT_SIZE.frame_width/2,height=DEFAULT_SIZE.frame_height*2,bg="blue")
        meld_frame.grid(row=0,column=1,rowspan=2,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.frame_list['meld_frame']=meld_frame
        
        message_frame = tk.Frame(self,width=DEFAULT_SIZE.frame_width/2,height=DEFAULT_SIZE.frame_height+50,bg="yellow")
        message_frame.grid(row=2,column=1,rowspan=2)
        message_frame.pack_propagate(False)
        
        self.messagebox=st.ScrolledText(message_frame,font = ("Times New Roman",20))
        self.messagebox.pack()
        
        player_frame=PlayerFrame(self,self.player)
        player_frame.grid(row=2,column=0,sticky=tk.N)
        self.frame_list['player_frame']=player_frame
        
        button_frame = tk.Frame(self,width=DEFAULT_SIZE.frame_width,height=50,bg="black")
        button_frame.grid(row=3,column=0)
        
        self.meld_button=tk.Button(button_frame,text="meld",command=self.play_cards)
        self.meld_button.pack(side="left")
        self.layout_button=tk.Button(button_frame,text="layout",command=self.layout)
        self.layout_button.pack(side="left")
        self.discard_button=tk.Button(button_frame,text="discard",command=self.discard)
        self.discard_button.pack(side="left")
        self.restart_button=tk.Button(button_frame,text="restart",command=self.restart)
        self.init_game()
        self.update_state(RummyGameState.DRAWCARD)
        
        self.player.point=0
        self.computer.point=0
        self.frame_list['player_frame'].title_label.config(text=f"Player is {self.player.point}")
        self.frame_list['computer_frame'].title_label.config(text=f"Computer is {self.computer.point}")

    
    def init_game(self):
        """init game and deal 10 cards each for player and computer"""
        
        self.update_state(RummyGameState.INIT)
        self.frame_list['stock_frame'].deck.shuffle()
        
        #deal 10 cards each for player and computer  
        for _ in range(10):
            card=self.frame_list['stock_frame'].deck.deal()
            #card.show=False
            self.frame_list['computer_frame']._add_card(card)
            self.frame_list['player_frame']._add_card(self.frame_list['stock_frame'].deck.deal())
        
        #sorted cards imglabel and build stock_frame imglabel
        self.frame_list['computer_frame'].sort_imglabel()    
        self.frame_list['player_frame'].sort_imglabel()
        self.frame_list['stock_frame'].create_deck()
        
           
    def discard(self) ->None:
        
        played_card: list[Card]=self.frame_list['player_frame'].get_picked_cards()
        if len(played_card) > 1:
            print("无效的卡牌")
            return 
        
        self.frame_list['player_frame'].destroy_picked_cards()    
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
        # if not self.check_goout():
        #     self.update_state(RummyGameState.DISCARD)
        self.check_goout()
    
    def layout(self):     
        played_card = self.frame_list['player_frame'].get_picked_cards()
        if len(played_card) > 1:
            print("无效的卡牌")
            return 
        played_card = played_card[0]
        
        layout_cards :list[tuple[list[Card],PlayerFrame]]= []
        for frame in self.meld_list:
            layout_cards.append((find_layout_cards(frame.player.cards),frame))
        
        print(layout_cards)
        del_index = None
        is_vaild = False
        for index,item in enumerate(layout_cards):
            if played_card in item[0]:
                self.frame_list['player_frame'].destroy_picked_cards()
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
            # score = cal_rummy_score(self.frame_list['computer_frame'].player.cards)
            # messagebox.showinfo("showinfo", f"winner is player score is {str(score)}")
            self.update_score()
            
        else:
            # score = cal_rummy_score(self.frame_list['player_frame'].player.cards)
            # messagebox.showinfo("showinfo", f"winner is computer score is {str(score)}")
            self.update_score(flag=False) 
            
    def update_messagebox(self,message:str) -> None:
        self.messagebox.configure(state ='normal')
        message+="\n" 
        self.messagebox.insert(tk.END,message)
        self.messagebox.see("end")
        self.messagebox.configure(state ='disabled')   
    
    def update_score(self,flag=True) -> None:
        """flag=true player win"""
        if flag:
            score = cal_rummy_score(self.frame_list['computer_frame'].player.cards)
            self.player.point+=score
            self.frame_list['player_frame'].title_label.config(text=f"Player is {self.player.point}")
            messagebox.showinfo("showinfo", f"winner is player score is {str(score)}")
        else:
            score = cal_rummy_score(self.frame_list['player_frame'].player.cards)
            self.computer.point+=score
            self.frame_list['computer_frame'].title_label.config(text=f"Computer is {self.computer.point}")
            messagebox.showinfo("showinfo", f"winner is computer score is {str(score)}")
                

    
    def update_state(self,state:RummyGameState,card: Card | None =None) -> None:
        if state == RummyGameState.PLAYING:
            self.meld_button.config(state="normal")
            self.discard_button.config(state="normal")
            self.layout_button.config(state="normal")
            self.frame_list['player_frame']._add_card(card)
            self.frame_list['player_frame'].sort_imglabel()
            self.state = RummyGameState.PLAYING 
        elif state == RummyGameState.DRAWCARD:
            self.frame_list['stock_frame'].state =RummyGameState.DRAWCARD
            self.state = RummyGameState.DRAWCARD
            self.meld_button.config(state="disabled")
            self.discard_button.config(state="disabled")
            self.layout_button.config(state="disabled")
        elif state == RummyGameState.GOOUT:
            self.frame_list['stock_frame'].state =RummyGameState.GOOUT
            self.state = RummyGameState.GOOUT
            self.show_winner()
            self.meld_button.pack_forget()
            self.discard_button.pack_forget()
            self.layout_button.pack_forget()
            self.restart_button.pack()                   
        elif state == RummyGameState.INIT:
            self.frame_list['stock_frame'].state =RummyGameState.INIT
            self.state = RummyGameState.INIT
            self.reset_all_widget()
            self.restart_button.pack_forget()
            self.meld_button.pack(side="left")
            self.layout_button.pack(side="left")
            self.discard_button.pack(side="left")
                       
    def computer_moves(self):
        
        #deal_card
        self.update_messagebox("-"*40)
        card = None
        discard_card = self.frame_list["stock_frame"].deck.cards[-1]
        
        if evaluate_discard(discard_card,self.frame_list["computer_frame"].player.cards):
            card = self.frame_list["stock_frame"]._deal_card_from_discard()
            self.update_messagebox(f"Computer deal {card} from discard pile")
        else:
            print(f"抽的是抽牌堆")
            card = self.frame_list["stock_frame"]._deal_card()
            self.update_messagebox(f"Computer deal card from stock")
        
        print(f"computer deal {card}")
        
        #card.show=False
        self.frame_list["computer_frame"]._add_card(card)
        
        #COMPUTER Playing either meld or check can lay out
        test = RummyAI(self.frame_list["computer_frame"].player.cards)
        
        while test.has_set() or test.has_run():
            # print(test.cards)
            # print(self.frame_list["computer_frame"].player.cards)
            
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
            test.recalculate()
            
                
        if self.state == RummyGameState.GOOUT:
            return
               
        self.computer_layout()

        if self.state == RummyGameState.GOOUT:
            return       
        
        self.computer_discard()
        self.check_goout()
    
    def computer_meld(self,indexlist):
        play_card = self.frame_list["computer_frame"].player.cards[indexlist[0]:indexlist[-1]+1]
        for card in play_card:
            card.show=True
        print(f"computer 有可以MELD的牌{play_card}")
        self.update_messagebox(f"Computer meld {play_card}")
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
        # print(layout_cards)
        while index<len(layout_cards) and len(layout_cards)>0:
            for card in layout_cards[index][0]:
                if card in self.frame_list["computer_frame"].player.cards:
                    card_index=self.frame_list["computer_frame"].player.cards.index(card)
                    print(f"computer has {card} for lay out")
                    self.update_messagebox(f"Computer lay out {card}")
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
        self.update_messagebox(f"Computer discard {discard}")
        self.frame_list['stock_frame'].create_discard_label(discard)
        self.frame_list['stock_frame'].deck.cards.append(discard)
        self.frame_list["computer_frame"].destroy_card_by_index([discard_index])
        self.frame_list["computer_frame"].reposition()
    
    def reset_all_widget(self):
        self.frame_list['stock_frame'].reset_deck()
        self.frame_list['player_frame'].reset()
        self.frame_list['computer_frame'].reset()
        self.meld_list.clear()
        self.frame_list['meld_frame'].clear_interior()
        
        
    def restart(self):
        
        self.init_game()
        self.update_state(RummyGameState.DRAWCARD)
                                              
    def create_setframe(self,played_card):
        temp_set = Player()
        set_frame=PlayerFrame(self.frame_list['meld_frame'].interior,temp_set,size=MELD_SIZE)
        set_frame.title_label.pack_forget()
        set_frame.pack_propagate(True)
        for card in played_card:
            set_frame._add_card(card)
        set_frame.sort_imglabel()
        
        set_frame.pack()
        self.frame_list['meld_frame'].canvas.update_idletasks()
        self.frame_list['meld_frame'].canvas.yview_moveto(1)
        
        if len(played_card) == 4 and rummy_is_set(played_card):
            return
        self.meld_list.append(set_frame)   


        
if __name__ == "__main__":
    root=tk.Tk()
    
    
    root.geometry("1200x950")
    RummyGame(root).pack(side="top", fill="both", expand=True)
    center(root)

    root.mainloop()
      