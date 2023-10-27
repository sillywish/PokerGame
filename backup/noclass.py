from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from cardgame import Card,Deck,Player,find_winner_simple

ROUND=1
deck=Deck()
computer=Player(name="Computer")
player=Player()
playerlist=[computer,player]
imglist=[]

deck.shuffle()
root = Tk()
root.geometry("1080x720")
root.configure(background="green")

# s = ttk.Style()
# s.configure('Red.TLabelframe.Label', font=('courier', 15, 'bold'))

COUNT=0



def shuffle_cards():
    global COUNT
    newlabel=Label(computer_frame,text=F"CARD :{COUNT}")
    COUNT+=1
    newlabel.pack(fill=Y)
    
def resize_cards(card:Card):
    filename=f"cards/{card.img_name}"
    card_img=Image.open(filename)
    global card_resize_img
    card_resize_img=card_img.resize((150,218))
    
    return card_resize_img


def create_computer_label(card:Card):
    global computer
    
    card_img = ImageTk.PhotoImage(resize_cards(card))
    computer.cards_img[card.symbol] = card_img
    if card.show is False:
        card_back_img=Image.open("cards/cardback.png")
        card_back_img=card_back_img.resize((150,218))
        card_img = ImageTk.PhotoImage(card_back_img)
        computer.cards_img["card"] = card_img
    
    imglabel=Label(computer_frame,image=card_img)
    imglabel.pack(padx=3,side=LEFT)
    
    computer.cards_labels.append(imglabel)
    
    

def create_player_label(card:Card):
    global player
    card_img = ImageTk.PhotoImage(resize_cards(card))
    player.cards_img[card.symbol] = card_img
    if card.show is False:
        card_back_img=Image.open("cards/cardback.png")
        card_back_img=card_back_img.resize((150,218))
        card_img = ImageTk.PhotoImage(card_back_img)
        player.cards_img["card"] = card_img
    imglabel=Label(player_frame,image=card_img)
    imglabel.pack(padx=3,side=LEFT)
    if card.show is False:
        imglabel.bind("<Button-1>",lambda event,card=card:display_card(card))
    player.cards_labels.append(imglabel)    

def display_card(card:Card):
    global player
    if card.show:
        
        player.cards_labels[0].config(image=player.cards_img["card"])
        card.show=False
    else:
        key=card.symbol
        player.cards_labels[0].config(image=player.cards_img[key])
        card.show=True

def show_result():
    global player,computer
    player.cards[0].show=True
    computer.cards[0].show=True
    player_sortedcards=player.sortedcards()
    computer_sortedcards=computer.sortedcards()
    

    #print(player.cards_img[key])
    for label in player.cards_labels:
        key=player_sortedcards[0].symbol
        label.config(image=player.cards_img[key])
        player_sortedcards.pop(0)

    for label in computer.cards_labels:
        key=computer_sortedcards[0].symbol
        label.config(image=computer.cards_img[key])
        computer_sortedcards.pop(0)
    #player.cards_labels[0].config(image=player.cards_img[key])
    # print(player.sortedcards())
    # print(computer.sortedcards())
    show_result_button.pack_forget()
    winner,fin_rank=find_winner_simple(playerlist)
    global winner_label
    if fin_rank[0][0].name == "Computer":
        
        computer_label.config(text=f"Computer is {fin_rank[0][0].category}")
        player_label.config(text=f"Player is {fin_rank[1][0].category}")
    else:
        computer_label.config(text=f"Computer is {fin_rank[1][0].category}")
        player_label.config(text=f"Player is {fin_rank[0][0].category}")
           
        #print(f"{player_rank[0]} \nWhich is {player_rank[0].category}")
    winner_label = Label(text=f"Winner is {winner.name}",font=("courier", 20,),bg="green")
    winner_label.pack()


def deal_cards(is_show:bool=True):
    global deck,playerlist
    for player in playerlist:
            card=deck.deal()
            card.show=is_show
            player.cards.append(card)
        
    create_computer_label(playerlist[0].cards[-1])
    create_player_label(playerlist[1].cards[-1])
    


def deal_cards_button():
    global ROUND
    if ROUND==1:
        deal_cards(False)
    
    deal_cards()

    global shuffle_button,show_result_button
    if ROUND==4:
        shuffle_button.pack_forget()
        #show_result()
        show_result_button=Button(root,text="result",command=show_result)
        show_result_button.pack()
           
    ROUND+=1 
    
#cards_img=resize_cards(f"/cards")
score_frame=Frame(root,width=200,height=500,bg="green")
score_frame.pack(padx=20,side=LEFT)  
# s = ttk.Style()
# s.configure('My.TFrame', background='red')
computer_frame=Frame(root,width=800,height=290,bd=0)
computer_frame.pack(pady=20)
computer_frame.pack_propagate(False)
# computer_frame.grid(row=0,column=0,padx=20,ipadx=20)
# computer_frame.grid_propagate(False)


player_frame=Frame(root,width=800,height=290,bd=0)
player_frame.pack(pady=20)
player_frame.pack_propagate(False)



computer_label = Label(computer_frame,text="Computer",font=("courier", 15))
computer_label.pack(pady=10)

player_label = Label(player_frame,text="Player",font=("courier", 15))
player_label.pack(pady=10,fill="x")

score_label = Label(score_frame,text="Your Point is 200",font=("courier", 15),bg="green")
score_label.pack(pady=10,fill="x")

shuffle_button = Button(root,text="deal_cards",command=deal_cards_button)
shuffle_button.pack()



#Define function to hide the widget
def hide_widget(widget:Widget):
   widget.pack_forget()

#Define a function to show the widget
def show_widget(widget:Widget):
   widget.pack()  


root.mainloop()