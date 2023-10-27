
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
        score_frame=Frame(self,width=150,height=500,)
        score_frame.pack(padx=15,side=LEFT)
        score_frame.pack_propagate(False) 
        self.widget_list["score_frame"]=score_frame

        computer_frame=Frame(self,width=800,height=290,bd=0)
        computer_frame.pack(pady=20)
        computer_frame.pack_propagate(False) 
        self.widget_list["computer_frame"]=computer_frame
        
        computer_card_frame=Frame(computer_frame,width=800,height=240,bd=0)
        self.widget_list["computer_card_frame"]=computer_card_frame


        player_frame=Frame(self,width=800,height=290,bd=0)
        player_frame.pack(pady=20)
        player_frame.pack_propagate(False)
        self.widget_list["player_frame"]=player_frame
        
        player_card_frame=Frame(player_frame,width=800,height=240,bd=0)
        self.widget_list["player_card_frame"]=player_card_frame
        
        button_frame=Frame(self,width=800,height=40,bd=0,bg="green")
        button_frame.pack()
        #button_frame.pack_propagate(False)
        self.widget_list["button_frame"]=button_frame
        
        
        #label area
        computer_label = Label(computer_frame,text="Computer",font=("courier", 15))
        computer_label.pack(pady=10)
        self.widget_list["computer_label"]=computer_label
        computer_card_frame.pack()

        player_label = Label(player_frame,text="Player",font=("courier", 15))
        player_label.pack(pady=10,fill="x")
        self.widget_list["player_label"]=player_label
        player_card_frame.pack()
        
        
        turn_label = Label(score_frame,text="Turn 0",font=("courier", 15),wraplength=150,height=3)
        turn_label.pack(pady=10,)
        self.widget_list["turn_label"]=turn_label

        score_label = Label(score_frame,text="Your Point is 100",font=("courier", 15),wraplength=150,height=5)
        score_label.pack(pady=10,)
        self.widget_list["score_label"]=score_label
        
        point_label = Label(score_frame,text="",font=("courier", 15),wraplength=150,height=5)
        point_label.pack(pady=10,)
        self.widget_list["point_label"]=point_label        
        
        winner_label = Label(score_frame,text="",font=("courier", 20,),wraplength=130,height=5)
        self.widget_list["winner_label"]=winner_label
        
        
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
        
    def create_computer_label(self,card:Card):
    
        card_img = ImageTk.PhotoImage(self.resize_cards(card))
        self.computer.cards_img[card.symbol] = card_img
        if card.show is False:
            card_back_img=Image.open("cards/cardback.png")
            card_back_img=card_back_img.resize((150,218))
            card_img = ImageTk.PhotoImage(card_back_img)
            self.computer.cards_img["card"] = card_img
        
        imglabel=Label(self.widget_list["computer_card_frame"],image=card_img)
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
        imglabel=Label(self.widget_list["player_card_frame"],image=card_img)
        imglabel.pack(padx=3,side=LEFT)
        #imglabel.place(anchor=CENTER)
        if card.show is False:
            imglabel.bind("<Button-1>",lambda event,card=card:self.display_card(card))
        self.player.cards_labels.append(imglabel)    


    def resize_cards(self,card:Card):
        filename=f"cards/{card.img_name}"
        card_img=Image.open(filename)
        card_resize_img=card_img.resize((150,218))  
        return card_resize_img
    

    def display_card(self,card:Card):
        if card.show:
            
            self.player.cards_labels[0].config(image=self.player.cards_img["card"])
            card.show=False
        else:
            key=card.symbol
            self.player.cards_labels[0].config(image=self.player.cards_img[key])
            card.show=True

    def show_result(self,):
        self.player.cards[0].show=True
        self.computer.cards[0].show=True
        player_sortedcards=self.player.sortedcards()
        computer_sortedcards=self.computer.sortedcards()
        
        
        for label in self.player.cards_labels:
            key=player_sortedcards[0].symbol
            label.config(image=self.player.cards_img[key])
            player_sortedcards.pop(0)

        for label in self.computer.cards_labels:
            key=computer_sortedcards[0].symbol
            label.config(image=self.computer.cards_img[key])
            computer_sortedcards.pop(0)

        
        self.widget_list["pass_button"].pack_forget()
        self.widget_list["add_point_button"].pack_forget()
        #show_result_button.pack_forget()
        winner,fin_rank=find_winner_simple(self.playerlist)
        if fin_rank[0][0].name == "Computer":
            
            self.widget_list["computer_label"].config(text=f"Computer is {fin_rank[0][0].category}")
            self.widget_list["player_label"].config(text=f"Player is {fin_rank[1][0].category}")
            self.player.point+=self.scoreboard.point*2
            self.update_scoreboard()
        else:
            self.widget_list["computer_label"].config(text=f"Computer is {fin_rank[1][0].category}")
            self.widget_list["player_label"].config(text=f"Player is {fin_rank[0][0].category}")
            
        self.widget_list["winner_label"].config(text=f"Winner is {winner.name}")
        self.widget_list["winner_label"].pack(pady=5,)
        
        
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
            
        self.create_computer_label(self.playerlist[0].cards[-1])
        self.create_player_label(self.playerlist[1].cards[-1])
        
    def pass_button(self,):

        if self.ROUND==5:
            self.show_result()
        else:
            self.deal_cards()
                    
        # if self.ROUND==4:
        #     self.widget_list["add_point_button"].pack_forget()
        #     self.widget_list["pass_button"].pack_forget()         
        #     self.widget_list["show_result_button"].pack(side=LEFT)
        #     self.widget_list["add_point_button"].pack(padx=10,side=LEFT)
            
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
        
        
        
    def clear_frame(self,frame):
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
        
        
        player_card_frame=self.widget_list["player_card_frame"]
        computer_card_frame=self.widget_list["computer_card_frame"]
        self.clear_frame(player_card_frame)
        self.clear_frame(computer_card_frame)
        
        self.widget_list["winner_label"].pack_forget()
        self.widget_list["restart_button"].pack_forget()
        self.widget_list["exit_button"].pack_forget()
        
        self.deal_cards(False)       
        self.deal_cards()
        self.ROUND=2
              
        self.widget_list["computer_label"].config(text="Computer")
        self.widget_list["player_label"].config(text="Player")        
        self.widget_list["pass_button"].pack(side=LEFT)
        if self.player.point>0:
            self.widget_list["add_point_button"].pack(padx=10,side=LEFT)
        

if __name__ == "__main__":
    root = Tk()
    root.geometry("1024x720")
    ShowHandGame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()  


