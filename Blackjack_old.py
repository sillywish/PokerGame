
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from cardgame import *

class BlackJackGame(Frame):
    
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.parent = parent
        self.config(bg="green")       
        # super().__init__(title="Black jack game",width=1024,height=720)
        self.ROUND=1
        self.deck=Deck()
        self.computer = Player(name="Computer")
        self.player = Player()
        self.player.point=50
        self.playerlist = [self.computer,self.player]
        self.scoreboard=PlayBoard(self.playerlist)
        self.turn=1
       
        
        self.widget_list = {}
        
        self.deck.shuffle()       
        self.ui_initialize()
       
        
    def ui_initialize(self):
        """Create Game User Interface"""        
        #frame area
        score_frame=Frame(self,width=150,height=500,)
        score_frame.pack(padx=15,side=LEFT)
        score_frame.pack_propagate(False) 
        self.widget_list["score_frame"]=score_frame
        

        computer_frame=Frame(self,width=800,height=290,bd=0,bg="green")
        computer_frame.pack(pady=20)
        computer_frame.pack_propagate(False) 
        self.widget_list["computer_frame"]=computer_frame
        
        computer_card_frame=Frame(computer_frame,width=800,height=240,bd=0,bg="green")
        self.widget_list["computer_card_frame"]=computer_card_frame


        player_frame=Frame(self,width=800,height=290,bd=0,bg="green")
        player_frame.pack(pady=20)
        player_frame.pack_propagate(False)
        self.widget_list["player_frame"]=player_frame
        
        player_card_frame=Frame(player_frame,width=800,height=240,bd=0,bg="green")
        self.widget_list["player_card_frame"]=player_card_frame
        
        button_frame=Frame(self,width=800,height=40,bd=0,bg="green")
        button_frame.pack()
        #button_frame.pack_propagate(False)
        self.widget_list["button_frame"]=button_frame
              
        #label area
        computer_label = Label(computer_frame,text="Computer",font=("courier", 15),bg="green")
        computer_label.pack(pady=10)
        self.widget_list["computer_label"]=computer_label
        computer_card_frame.pack()

        player_label = Label(player_frame,text="Player",font=("courier", 15),bg="green")
        player_label.pack(pady=10,fill="x")
        self.widget_list["player_label"]=player_label
        player_card_frame.pack()
        
        
        turn_label = Label(score_frame,text="Turn 0",font=("courier", 15),wraplength=150,height=3)
        turn_label.pack(pady=10,)
        self.widget_list["turn_label"]=turn_label

        score_label = Label(score_frame,text=f"Your Point is {self.player.point}",font=("courier", 15),wraplength=150,height=5)
        score_label.pack(pady=10,)
        self.widget_list["score_label"]=score_label
        
        point_label = Label(score_frame,text="",font=("courier", 15),wraplength=150,height=5)
        point_label.pack(pady=10,)
        self.widget_list["point_label"]=point_label        
        
        winner_label = Label(score_frame,text="",font=("courier", 20,),wraplength=130,height=5)
        self.widget_list["winner_label"]=winner_label
        
        
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
        
 
    
    def resize_cards(self,card:Card):
        filename=f"cards/{card.img_name}"
        card_img=Image.open(filename)
        card_resize_img=card_img.resize((150,218))  
        return card_resize_img
        
    def create_computer_label(self,card:Card):
    
        card_img = ImageTk.PhotoImage(self.resize_cards(card))
        self.computer.cards_img[card.symbol] = card_img
        if card.show is False:
            card_back_img=Image.open("cards/cardback.png")
            card_back_img=card_back_img.resize((150,218))
            card_img = ImageTk.PhotoImage(card_back_img)
            self.computer.cards_img["card"] = card_img
        
        imglabel=Label(self.widget_list["computer_card_frame"],image=card_img,bg="green")
        imglabel.pack(padx=3,side=LEFT)
        
        self.computer.cards_labels.append(imglabel)
    

    def create_player_label(self,card:Card):
        card_img = ImageTk.PhotoImage(self.resize_cards(card))
        self.player.cards_img[card.symbol] = card_img
        if card.show is False:
            card_back_img=Image.open("cards/cardback.png")
            card_back_img=card_back_img.resize((150,218))
            card_img = ImageTk.PhotoImage(card_back_img)
            self.player.cards_img["card"] = card_img
        imglabel=Label(self.widget_list["player_card_frame"],image=card_img,bg="green")
        imglabel.pack(padx=3,side=LEFT)
        #imglabel.place(anchor=CENTER)
        if card.show is False:
            imglabel.bind("<Button-1>",lambda event,card=card:self.display_card(card))
        self.player.cards_labels.append(imglabel)    



    

    def display_card(self,card:Card):
        if card.show:
            
            self.computer.cards_labels[0].config(image=self.computer.cards_img["card"])
            card.show=False
        else:
            key=card.symbol
            self.computer.cards_labels[0].config(image=self.computer.cards_img[key])
            card.show=True

    def deal_cards(self,player:Player,is_show: bool=True,round:int=1):
        
        for _ in range(round):
            card=self.deck.deal()
            card.show=is_show
            player.cards.append(card)
            cal_blackjack(player)
            
            if player.name == "Computer":                       
                self.create_computer_label(card)
            else:
                self.create_player_label(card)
        

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
            self.display_card(self.computer.cards[0])
            self.update_winner(self.computer)
            self.updata_button()
            self.check_game_end()
        
        self.widget_list["surrender_button"].config(state="disabled")
            #winner=self.blackjack.find_winner(self.computer,self.player)        
    
    def stand(self):
        self.computer_bot()
        self.display_card(self.computer.cards[0])
        winner=find_blackjack_winner(self.computer,self.player)
        self.update_winner(winner)
        self.updata_button()
        self.check_game_end()
    
        
    
    def double_down(self):
        pass
    
    def surrender(self):
            
        self.updata_button()
        if self.check_game_end():
            pass
        else:
            self.restart()
    
      
        
    def update_scoreboard(self):
        self.widget_list["score_label"].config(text=f"Your point is {str(self.player.point)}")
        self.widget_list["point_label"].config(text=f"Bet point is {str(self.scoreboard.point)}")
    
    def update_winner(self,winner:Optional[Player]):
        if winner:
            if winner.name != "Computer":
                winner.point+=self.scoreboard.point*2
            self.widget_list["winner_label"].config(text=f"Winner is {winner.name}")
            self.widget_list["winner_label"].pack()
        else:
            self.widget_list["winner_label"].config(text=f"It is tie")
            self.widget_list["winner_label"].pack()
            self.player.point+=self.scoreboard.point
        
        self.widget_list["computer_label"].config(text=f"Computer is {self.computer.blackjack_point}")
        self.widget_list["player_label"].config(text=f"Player is {self.player.blackjack_point}") 
        self.update_scoreboard()
        
    def updata_button(self):

        self.widget_list["hit_button"].pack_forget()
        self.widget_list["stand_button"].pack_forget()    
        self.widget_list["surrender_button"].pack_forget()
        self.widget_list["restart_button"].pack(side=LEFT)
        
                    
    def clear_frame(self,frame):
        for widget in frame.winfo_children():
             widget.destroy()     
    def game_start(self):
        self.deck.shuffle()
        self.scoreboard.reset()
        self.scoreboard.init_point()
        self.deal_cards(self.player,round=2)
        self.deal_cards(self.computer,is_show=False)
        self.deal_cards(self.computer)      
        self.update_scoreboard()
        self.widget_list["start_button"].pack_forget()
        self.widget_list["hit_button"].pack(side=LEFT)
        self.widget_list["stand_button"].pack(padx=10,side=LEFT)
        self.widget_list["surrender_button"].pack(side=LEFT)
        self.widget_list["turn_label"].config(text=f"Turn {str(self.turn)}")       
        self.ROUND+=1

        
    def restart(self):
        self.computer.reset_cards()
        self.player.reset_cards()
        self.deck.reset()
        self.deck.shuffle()
        self.scoreboard.reset()
        self.scoreboard.init_point()
        self.update_scoreboard()
        self.widget_list["turn_label"].config(text=f"Turn {str(self.turn)}")
        
        
        player_card_frame=self.widget_list["player_card_frame"]
        computer_card_frame=self.widget_list["computer_card_frame"]
        self.clear_frame(player_card_frame)
        self.clear_frame(computer_card_frame)
        
        self.deal_cards(self.player,round=2)
        self.deal_cards(self.computer,is_show=False)
        self.deal_cards(self.computer)
        
        self.widget_list["winner_label"].pack_forget()
        self.widget_list["restart_button"].pack_forget()
        self.widget_list["exit_button"].pack_forget()
        
        self.widget_list["computer_label"].config(text="Computer")
        self.widget_list["player_label"].config(text="Player")       
        self.widget_list["hit_button"].pack(side=LEFT)
        self.widget_list["stand_button"].pack(padx=10,side=LEFT)
        self.widget_list["surrender_button"].config(state="normal")
        self.widget_list["surrender_button"].pack(side=LEFT)

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
    # game= BlackJackGame()
    # game.run()   


