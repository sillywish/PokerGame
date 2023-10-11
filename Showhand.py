
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from cardgame import PlayBoard,Card,Deck,Player,find_winner_simple
from customwidget import PlayerFrame

class ShowHandGame(Frame):
    
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.parent = parent
        self.config(bg="green") 
        self.ROUND=1
        self.deck=Deck()
        self.computer = Player(name="Computer")
        self.player = Player()
        self.playerlist = [self.computer,self.player]
        self.scoreboard=PlayBoard(self.playerlist)
        self.turn=1
        self.widget_list: dict[str,PlayerFrame|Frame|Label|Button]= {}
        
        self.deck.shuffle()       
        self.ui_initialize()

    def score_reset(self):
        self.player.point=100
        
        
    def ui_initialize(self):
        """Create Game User Interface"""        
        #frame area
        score_frame=Frame(self,width=150,height=500,bg="green")
        score_frame.pack(padx=15,side=LEFT)
        score_frame.pack_propagate(False) 
        self.widget_list["score_frame"]=score_frame
           
        computer_frame=PlayerFrame(self,self.computer)
        self.widget_list["computer_frame"]=computer_frame
        
        winner_frame=Frame(self,width=800,height=40,bg="green")
        winner_frame.pack()
        self.widget_list["winner_frame"]=winner_frame
        
        player_frame=PlayerFrame(self,self.player)
        self.widget_list["player_frame"]=player_frame
        
  
        button_frame=Frame(self,width=800,height=40,bd=0,bg="green")
        button_frame.pack()
        #button_frame.pack_propagate(False)
        self.widget_list["button_frame"]=button_frame
        
        
        #label area 
        turn_label = Label(score_frame,text="Turn 0",font=("courier", 15),wraplength=150,height=3,bg="green")
        turn_label.pack(pady=10,)
        self.widget_list["turn_label"]=turn_label

        score_label = Label(score_frame,text="Your Point is 100",font=("courier", 15),wraplength=150,height=5,bg="green")
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
        start_button.pack()
        self.widget_list["start_button"]=start_button
        
        pass_button = Button(button_frame,width=20,text="pass",command=self.pass_button)
        #pass_button.pack()
        self.widget_list["pass_button"]=pass_button
               
        restart_button = Button(button_frame,width=20,text="restart",command=self.restart)
        self.widget_list["restart_button"]=restart_button
        
        add_point_button = Button(button_frame,width=20,text="addpoint",command=self.add_point)
        self.widget_list["add_point_button"]=add_point_button
        
        show_result_button=Button(button_frame,width=20,text="result",command=self.show_result)
        self.widget_list["show_result_button"]=show_result_button
        
        exit_button=Button(button_frame, width=20,text="Quit", command=self.parent.destroy)#button to close the window
        self.widget_list["exit_button"]=exit_button
            
    def show_result(self,):
        self.player.cards[0].show=True
        self.computer.cards[0].show=True
        
        self.widget_list["computer_frame"].sort_imglabel()
        self.widget_list["player_frame"].sort_imglabel()
                
        self.widget_list["pass_button"].pack_forget()
        self.widget_list["add_point_button"].pack_forget()
        winner,fin_rank=find_winner_simple(self.playerlist)
        if fin_rank[0][0].name == "Computer":
            
            self.widget_list["computer_frame"].title_label.config(text=f"Computer is {fin_rank[0][0].category}")
            self.widget_list["player_frame"].title_label.config(text=f"Player is {fin_rank[1][0].category}")
            self.player.point+=self.scoreboard.point*2
            self.update_scoreboard()
        else:
            self.widget_list["computer_frame"].title_label.config(text=f"Computer is {fin_rank[1][0].category}")
            self.widget_list["player_frame"].title_label.config(text=f"Player is {fin_rank[0][0].category}")
            
        self.widget_list["winner_label"].config(text=f"Winner is {winner.name}")
        #self.widget_list["winner_label"].pack(pady=5,)
        
        
        if self.player.point==0 or self.turn>10:
            self.popup(flag=0)
            self.score_reset()
            self.widget_list["restart_button"].config(text="restart")  
            self.widget_list["restart_button"].pack(side=LEFT)
            self.widget_list["exit_button"].pack(padx=10,side=LEFT)
            self.turn=1
        elif self.player.point>=200:
            self.popup(flag=1)
            self.score_reset()
            self.widget_list["restart_button"].config(text="restart")  
            self.widget_list["restart_button"].pack(side=LEFT)
            self.widget_list["exit_button"].pack(padx=10,side=LEFT)
            self.turn=1
        else:
            self.widget_list["restart_button"].config(text="next turn")  
            self.widget_list["restart_button"].pack(side=LEFT)
            self.turn+=1
            
        
    def deal_cards(self,is_show:bool=True):
        for player in self.playerlist:
            card=self.deck.deal()
            card.show=is_show
            player.cards.append(card)            
            if player.name == "Computer":
                self.widget_list["computer_frame"].create_cardimg_label(card,flag=False)                       
            else:
                self.widget_list["player_frame"].create_cardimg_label(card)
             
    def pass_button(self,):

        if self.ROUND==5:
            self.show_result()
        else:
            self.deal_cards()
                               
        if self.player.point==0:
            self.widget_list["add_point_button"].pack_forget()
                   
        self.ROUND+=1 
    
    def add_point(self):
        self.scoreboard.point+=10
        self.player.point-=10
        self.update_scoreboard()
        
        if self.ROUND==5:
            self.show_result()          
        else:
            self.deal_cards()
             
        if self.player.point==0:
            self.widget_list["add_point_button"].pack_forget()
                               
        self.ROUND+=1
        
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
        
        
        
    def clear_frame(self,frame:Frame):
        for widget in frame.winfo_children():
             widget.destroy() 
     
    def game_start(self):
        self.deck.shuffle()
        self.scoreboard.reset()
        self.scoreboard.init_point()
        self.deal_cards(False)       
        self.deal_cards()
        self.update_scoreboard()
        self.widget_list["start_button"].pack_forget()
        self.widget_list["pass_button"].pack(side=LEFT)
        self.widget_list["add_point_button"].pack(padx=10,side=LEFT)
        self.widget_list["turn_label"].config(text=f"Turn {str(self.turn)}")
        
        self.ROUND+=1
    
    def update_scoreboard(self):
        self.widget_list["score_label"].config(text=f"Your point is {str(self.player.point)}")
        self.widget_list["point_label"].config(text=f"Bet point is {str(self.scoreboard.point)}")
    
    def restart(self):
        self.computer.reset_cards()
        self.player.reset_cards()
        self.deck.reset()
        self.deck.shuffle()
        self.scoreboard.reset()
        self.scoreboard.init_point()
        self.update_scoreboard()
        self.widget_list["turn_label"].config(text=f"Turn {str(self.turn)}")
        
        
        player_card_frame=self.widget_list["player_frame"].card_frame
        computer_card_frame=self.widget_list["computer_frame"].card_frame
        self.clear_frame(player_card_frame)
        self.clear_frame(computer_card_frame)
        

        self.widget_list["restart_button"].pack_forget()
        self.widget_list["exit_button"].pack_forget()
        self.widget_list["winner_label"].config(text="")
        
        self.deal_cards(False)       
        self.deal_cards()
        self.ROUND=2
              
        self.widget_list["computer_frame"].title_label.config(text="Computer")
        self.widget_list["player_frame"].title_label.config(text="Player")        
        self.widget_list["pass_button"].pack(side=LEFT)
        if self.player.point>0:
            self.widget_list["add_point_button"].pack(padx=10,side=LEFT)
        

if __name__ == "__main__":
    root = Tk()
    root.geometry("1024x720")
    ShowHandGame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()  


