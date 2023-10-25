
from tkinter import *
from tkinter import ttk

from cardgame import *
from customwidget import PlayerFrame


class BlackJackGame(Frame):
    
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.parent = parent
        self.config(bg="green")       
        self.deck=Deck()
        self.computer = Player(name="Computer")
        self.player = Player()
        self.player.point=50
        self.scoreboard=PlayBoard([self.computer,self.player])
        self.turn=1
        self.state=PokerGameState.INIT 
        self.widget_list: dict[str,PlayerFrame|Frame|Label|Button]= {}
        
        self.deck.shuffle()       
        self.ui_initialize()
       
    def set_state(self,state:PokerGameState):
        self.state=state
        
    def ui_initialize(self):
        """Create Game User Interface"""        
        #frame area
        score_frame=Frame(self,width=150,height=700,bg="green")
        score_frame.pack(padx=15,side=LEFT)
        score_frame.pack_propagate(False) 
        self.widget_list["score_frame"]=score_frame
        

        
        computer_frame=PlayerFrame(self,self.computer)
        computer_frame.pack(pady=10)
        self.widget_list["computer_frame"]=computer_frame
        
        winner_frame=Frame(self,width=800,height=40,bg="green")
        winner_frame.pack()
        self.widget_list["winner_frame"]=winner_frame
        
        player_frame=PlayerFrame(self,self.player)
        player_frame.pack()
        self.widget_list["player_frame"]=player_frame
        
    
        button_frame=Frame(self,width=800,height=40,bd=0,bg="green")
        button_frame.pack()
        #button_frame.pack_propagate(False)
        self.widget_list["button_frame"]=button_frame
              
        #label area

        turn_label = Label(score_frame,text="Turn 0",font=("courier", 15),wraplength=150,height=3,bg="green")
        turn_label.pack(pady=10,)
        self.widget_list["turn_label"]=turn_label

        score_label = Label(score_frame,text=f"Your Point is {self.player.point}",font=("courier", 15),wraplength=150,height=5,bg="green")
        score_label.pack(pady=10,)
        self.widget_list["score_label"]=score_label
        
        point_label = Label(score_frame,text="",font=("courier", 15),wraplength=150,height=5,bg="green")
        point_label.pack(pady=10,)
        self.widget_list["point_label"]=point_label        
        
        winner_label = Label(winner_frame,text="",font=("courier", 20,),bg="green")
        self.widget_list["winner_label"]=winner_label
        winner_label.pack()
        
        
        #button area

        start_button = Button(button_frame,width=20,text="start",command=self.game_start)
        start_button.pack(pady=10,side=LEFT)
        self.widget_list["start_button"]=start_button
        
               
        restart_button = Button(button_frame,width=20,text="restart",command=self.restart)
        self.widget_list["restart_button"]=restart_button
    
        hit_button = Button(button_frame,width=20,text="hit",command=self.hit)
        self.widget_list["hit_button"]=hit_button
        
        stand_button = Button(button_frame,width=20,text="stand",command=self.stand)
        self.widget_list["stand_button"]=stand_button
        
        surrender_button = Button(button_frame,width=20,text="surrender",command=self.surrender)
        self.widget_list["surrender_button"]=surrender_button
        
        exit_button=Button(button_frame, width=20,text="Quit", command=self.parent.destroy)#button to close the window
        self.widget_list["exit_button"]=exit_button
               
    def deal_cards(self,player:Player,is_show: bool=True,round:int=1):
        
        for _ in range(round):
            card=self.deck.deal()
            card.show=is_show
            player.cards.append(card)
            cal_blackjack(player)
            
            if player.name == "Computer":
                self.widget_list["computer_frame"].create_cardimg_label(card,flag=False)                       
            else:
                self.widget_list["player_frame"].create_cardimg_label(card,flag=False)
       
    def popup(self,flag):
        pop=Toplevel(self)
        pop.geometry("200x200") 
        x = self.winfo_x()
        y = self.winfo_y()
        pop.geometry("+%d+%d" % (x + 400, y + 200))
            
        if flag==0:
            result_lable=Label(pop,text="Game Over",font=("courier", 20,))
            result_lable.pack()
        else:
            result_lable=Label(pop,text="You Win !!",font=("courier", 20,))
            result_lable.pack()
            
        turn_lable=Label(pop,text=f"You use {str(self.turn)} turn",font=("courier", 20,),wraplength=200)
        turn_lable.pack()  
       
    def computer_bot(self):
        while self.computer.blackjack_point<=14:
            self.deal_cards(self.computer)
        
    def hit(self):
               
        self.deal_cards(self.player)
        
        if self.player.blackjack_point>21:           
            self.update_winner(self.computer)
            self.set_state(PokerGameState.FINSIHED)
            self.update_button()
        
        elif len(self.player.cards)>=5:
            self.update_winner(self.player)
            self.set_state(PokerGameState.FINSIHED)
            self.update_button()
            
        self.set_state(PokerGameState.PLAYING)
        self.update_button()   
        #self.widget_list["surrender_button"].config(state="disabled")
                      
    def stand(self):
        self.computer_bot()
        winner=find_blackjack_winner(self.computer,self.player)
        self.update_winner(winner)
        self.set_state(PokerGameState.FINSIHED)
        self.update_button()
      
    def double_down(self):
        pass
    
    def surrender(self):       
        self.set_state(PokerGameState.FINSIHED)
        self.update_button()
                
    def update_scoreboard(self):
        self.widget_list["score_label"].config(text=f"Your point is {str(self.player.point)}")
        self.widget_list["point_label"].config(text=f"Bet point is {str(self.scoreboard.point)}")
    
    def update_winner(self,winner:Optional[Player]):
        if winner:
            if winner.name != "Computer":
                winner.point+=self.scoreboard.point*2
            self.widget_list["winner_label"].config(text=f"Winner is {winner.name}")
        else:
            self.widget_list["winner_label"].config(text=f"It is tie")
            self.player.point+=self.scoreboard.point
        
        self.widget_list["computer_frame"].title_label.config(text=f"Computer is {self.computer.blackjack_point}")
        self.widget_list["player_frame"].title_label.config(text=f"Player is {self.player.blackjack_point}") 
        self.update_scoreboard()
        
    def update_button(self):
             
        if self.state == PokerGameState.START:
            self.widget_list["start_button"].pack_forget()
            self.widget_list["hit_button"].pack(pady=10,side=LEFT)
            self.widget_list["stand_button"].pack(pady=10,padx=10,side=LEFT)
            self.widget_list["surrender_button"].pack(pady=10,side=LEFT)
            self.widget_list["turn_label"].config(text=f"Turn {str(self.turn)}")
            
        elif self.state == PokerGameState.PLAYING:
            self.widget_list["surrender_button"].config(state="disabled")
            
        elif self.state == PokerGameState.FINSIHED:
            self.widget_list["computer_frame"].display_card(self.computer.cards[0])

            self.widget_list["hit_button"].pack_forget()
            self.widget_list["stand_button"].pack_forget()    
            self.widget_list["surrender_button"].pack_forget()
            self.widget_list["restart_button"].pack(pady=10,side=LEFT) 
            self.check_game_end()
            
        elif self.state == PokerGameState.RESTART:
            #self.widget_list["winner_label"].pack_forget()
            self.widget_list["restart_button"].pack_forget()
            self.widget_list["exit_button"].pack_forget() 
            self.widget_list["winner_label"].config(text="")    
            self.widget_list["computer_frame"].title_label.config(text="Computer")
            self.widget_list["player_frame"].title_label.config(text="Player")    
            self.widget_list["hit_button"].pack(pady=10,side=LEFT)
            self.widget_list["stand_button"].pack(pady=10,padx=10,side=LEFT)
            self.widget_list["surrender_button"].config(state="normal")
            self.widget_list["surrender_button"].pack(pady=10,side=LEFT)
            self.widget_list["turn_label"].config(text=f"Turn {str(self.turn)}")
                       
        self.update_scoreboard()
                                                    
    def game_start(self):
        self.deck.shuffle()
        self.scoreboard.reset()
        self.scoreboard.init_point()
        self.deal_cards(self.player,round=2)
        self.deal_cards(self.computer,is_show=False)
        self.deal_cards(self.computer)      
        self.set_state(PokerGameState.START)
        self.update_button()      
        
    def restart(self):
        self.computer.reset_cards()
        self.player.reset_cards()
        self.deck.reset()
        self.deck.shuffle()
        self.scoreboard.reset()
        self.scoreboard.init_point()
              
        self.widget_list["player_frame"].clear_cardframe()
        self.widget_list["computer_frame"].clear_cardframe()
        
        self.deal_cards(self.player,round=2)
        self.deal_cards(self.computer,is_show=False)
        self.deal_cards(self.computer)
        
        self.set_state(PokerGameState.RESTART)
        self.update_button()        

    def check_game_end(self) -> bool:
        if self.player.point==0:
            self.popup(flag=0)
            self.widget_list["exit_button"].pack(padx=10,side=LEFT)
            self.turn=1
            self.player.point=50
            return True
        elif self.player.point>=100:
            self.popup(flag=1)
            self.player.point=50
            self.widget_list["exit_button"].pack(padx=10,side=LEFT)
            self.turn=1
            return True
        else:
            
            self.turn+=1
            return False

if __name__ == "__main__":

    
    root = Tk()
    root.geometry("1024x720")
    BlackJackGame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


