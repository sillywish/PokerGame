import random
import numpy as np
import os
from enum import Enum,auto
from copy import deepcopy
from typing import Any,Optional
from tkinter import Label

SUITS={'hearts':"♡",'diamonds':"♢",'spades':"♠",'clubs':"♣"}
VALUES={
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5,
        "Six":6,
        "Seven":7,
        "Eight":8,
        "Nive":9,
        "Ten":10,
        "Jack":11,
        "Queen":12,
        "King":13,
        "Ace":14,
    }  


class Card:
    def __init__(self,
                 suit:str,
                 value:int,
                 name:str,
                 symbol:str) -> None:
        
        self.suit: str = suit
        self.value: int = value       
        self.name: str = name
        self.symbol: str =symbol
        self.show: bool = True
        self.num: int = self.cal_num()
        

    def __repr__(self) -> str:
        if self.show:
            return f"{self.symbol}"
        else:
            return "card"
        
    @property   
    def img_name(self) -> str:
        return f"{str(self.value)}_of_{self.suit}.png"
    
    def cal_num(self) -> int:
        if self.suit == "clubs":
            return self.value+14
        elif self.suit == "spades":
            return self.value+14*2
        elif self.suit == "hearts":
            return self.value+14*3
        else:
            return self.value
class Deck:
    __suits={'hearts':"♡",'diamonds':"♢",'spades':"♠",'clubs':"♣"}
    __values={
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5,
        "Six":6,
        "Seven":7,
        "Eight":8,
        "Nive":9,
        "Ten":10,
        "Jack":11,
        "Queen":12,
        "King":13,
        "Ace":14,
    }


    def __init__(self) -> None:
        self.cards=[]
        
                
        for suit in self.__suits:
            for name in self.__values:
                if self.__values[name]>10:
                    symbol=name[0]+self.__suits[suit]
                    card=Card(suit,self.__values[name],name,symbol)
                else:
                    symbol=str(self.__values[name])+self.__suits[suit]
                    card=Card(suit,self.__values[name],name,symbol)
                
                self.cards.append(card)

    def __repr__(self) -> str:
        return f"Deck of cards: {len(self.cards)} remaining"
    
    def reset(self):
        self.cards=[]        
        for suit in self.__suits:
            for name in self.__values:
                if self.__values[name]>10:
                    symbol=name[0]+self.__suits[suit]
                    card=Card(suit,self.__values[name],name,symbol)
                else:
                    symbol=str(self.__values[name])+self.__suits[suit]
                    card=Card(suit,self.__values[name],name,symbol)
                
                self.cards.append(card)
      
    def shuffle(self) -> None:
        random.shuffle(self.cards)
        

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def num_of_crads(self) -> int:
        return len(self.cards)
    
    def deal(self) -> Card:
        return self.cards.pop()

class Player:
    def __init__(self,name:str = "Player") -> None:
        
        self.cards: list[Card]=[]
        self.point: int = 100
        self.blackjack_point: Optional[int] = None
        self.name:str=name
        self.category:str="Unkonw"
        self.cards_img:dict={}
        self.cards_labels: list[CardLabel]=[]
        #self.values: list[int]=[]

    def __repr__(self) -> str:
        return f"{self.name} has cards {self.cards}"
    
    @property
    def final_cat(self):
        return f"{self.name} is {self.category}"

    def reset_cards(self):
        self.cards.clear()
        self.cards_img.clear()
        self.cards_labels.clear()
        self.category = "Unkonw"


    def _sortedcards(self) -> list[Card]:
        sorted_cards=[]
        temp_cards=deepcopy(self.cards)
        
        while len(temp_cards)>0:
            mincard=temp_cards[0]
            index=0
            for i in range(1,len(temp_cards)):
                if temp_cards[i].value<mincard.value:
                    mincard=temp_cards[i]
                    index=i
            sorted_cards.append(mincard)
            temp_cards.remove(temp_cards[index])

        return sorted_cards   
  
    #bubble_sort
    def sortedcards(self) ->None:
        """Bubble sort"""
        length = len(self.cards)
        
        if length < 1:
            return
        
        for i in range(length):
            is_swap = False
            for j in range(length - i -1):
                if self.cards[j].value > self.cards[j+1].value:
                    self.cards[j], self.cards[j+1] = self.cards[j+1], self.cards[j]
                    is_swap=True
            if not is_swap:
                break
            
    def sortedcards_by_num(self) ->None:
        """Bubble sort by card.num"""
        length = len(self.cards)
        
        if length < 1:
            return
        
        for i in range(length):
            is_swap = False
            for j in range(length - i -1):
                if self.cards[j].num > self.cards[j+1].num:
                    self.cards[j], self.cards[j+1] = self.cards[j+1], self.cards[j]
                    is_swap=True
            if not is_swap:
                break
                    
class PokerScore:
    """Hand-ranking categories that differ by suit alone"""
    def __init__(self,cards:list[Card]) -> None:
        self.cards:list[Card]=cards
        self.values=sorted([card.value for card in self.cards])
        self.suits=[card.suit for card in self.cards]
        self.category:str="Unkown"

    def get_score(self) ->list[Any]:
        """ return ranklist:[(9,),...]

        first tuple is the rank of category:
        9 -> straight flush
        8 -> four kind
        7 -> fullhouse
        6 -> flush
        5 -> straight
        4 -> threekind
        3 -> two pair
        2 -> one pair
        1 -> high card
        
        """
        ranklist:list[tuple]=[]
        for v in set(self.values):
            ranklist.append((self.values.count(v),v))
        ranklist=sorted(ranklist)
        
        if self.straight() and self.flush():
            ranklist.append((9,)) 
            self.category="straight flush"           
            #print("同花顺")
        elif self.fourkind():
            ranklist.append((8,))
            self.category="four kind" 
            #print("四条")
        elif self.fullhouse():
            ranklist.append((7,))
            self.category="full house" 
            #print("俘虏")
        elif self.flush():
            ranklist.append((6,))
            self.category="flush" 
            #print("同花")
        elif self.straight():
            ranklist.append((5,))
            self.category="straight" 
            #print("顺子")
        elif self.threekind():
            ranklist.append((4,))
            self.category="three kind" 
            #print("三条")
        elif self.twopair():
            ranklist.append((3,))
            self.category="two pair" 
            #print("两对")
        elif self.onepair():
            ranklist.append((2,))
            self.category="one pair" 
            #print("一对")
        else:
            ranklist.append((1,))
            self.category="high card" 
            #print("散牌")
        
        return ranklist[::-1]

    def straight(self) ->bool:
        
        return self.checkConsecutive(self.values)

    def flush(self) -> bool:
        if len(set(self.suits))==1:
            return True
        else:
            return False
        
    def fourkind(self) -> bool:
        if len(set(self.values))!=2:
            return False
        for v in set(self.values):
            if self.values.count(v)==1 or self.values.count(v)==4:
                return True
        return False
        
    def fullhouse(self) -> bool:
        if len(set(self.values))!=2:
            return False
        for v in set(self.values):
            if self.values.count(v)==2 or self.values.count(v)==3:
                return True
        return False
        
    def threekind(self) -> bool:
        if len(set(self.values))!=3:
            return False
        for v in set(self.values):
            if self.values.count(v)==3:
                return True
        return False
    
    def twopair(self) -> bool:
        if len(set(self.values))!=3:
            return False
        for v in set(self.values):
            if self.values.count(v)==2:
                return True
        return False

    def onepair(self) -> bool:
        if len(set(self.values))==4:
            return True
        return False

    def highcardvalue(self):
        suits={'hearts':3,'diamonds':1,'spades':4,'clubs':2}
        highcard=None
        for card in self.cards:
            if highcard is None:
                highcard=card
            else:
                if highcard.value < card.value:                    
                    highcard = card
                elif highcard.value == card.value:
                    if suits[highcard.suit] < suits[card.suit]:
                        highcard = card

        return highcard

    
    def checkConsecutive(self,cards_value:list[int]) ->bool:
        ##ace can be 1 or 14
        if len(set(cards_value))!=5:
            return False
        n = len(cards_value) - 1
        if 14 in cards_value:
            newcards_value=[]
            for value in cards_value:
                if value==14:
                    newcards_value.append(1)
                else:
                    newcards_value.append(value)
            
            return (sum(np.diff(cards_value) == 1) >= n) or (sum(np.diff(sorted(newcards_value)) == 1) >= n)

        return (sum(np.diff(cards_value) == 1) >= n)

class PlayBoard:
    def __init__(self,playlist:list[Player],basepoint:int=10) -> None:
        self.point: int=0
        self.basepoint: int =basepoint
        self.playerlist: list[Player]=playlist
    
    def __repr__(self) -> str:
        return f"Bet point is {self.point}"
    
    def reset(self):
        self.point=0

    def init_point(self):
        self.point=self.basepoint
        for player in self.playerlist:
            player.point-=self.basepoint

class BaseMenu:
    def __init__(self) -> None:
        
        pass

class PokerGameState(Enum):
    
    INIT = auto()
    START = auto()
    PLAYING = auto()
    FINSIHED = auto()
    RESTART = auto()

class RummyGameState(Enum):
    DRAWCARD = auto()
    PLAYING = auto()
    DISCARD = auto()
    GOOUT = auto()
    SCORE = auto()
    
class CardLabel(Label):
    def __init__(self,parent,card,position,*args, **kwargs):
        Label.__init__(self,parent,*args, **kwargs)
        self.state: CardState = CardState.NORMAL
        self.card: Card =card
        self.position : int = position
           
class CardState(Enum):
    NORMAL = auto()
    PICK = auto()      
    
    
class RummyAI:
    def __init__(self,hands: list[Card]) -> None:
        self.cards = hands
        self.values=sorted([card.value for card in self.cards])
        self.nums=sorted([card.num for card in self.cards])
        self.suits=[card.suit for card in self.cards]
    
        
        
    def has_set(self) -> None | list[int]:
        """默认cards已经根据value排序"""
        index= 1
        count=1
        has_set=False
        startindex=0
        result_set=None
        current_value= self.values[0]
        for value in self.values[1:]:
            if value == current_value:
                count+=1
                if count >=3:
                    has_set=True
                    result_set=[i for i in range(startindex,index+1)]
            else:
                
                current_value = value
                startindex = index
                if has_set:
                    break
                count=1
            index+=1 
                
        # for value in set(self.values):
        #     if self.values.count(value)>=3:
        #         return True
        
        return result_set


    def has_run(self) -> None| list[int]:
        """默认列表已经根据card.num进行排序 并且没有重复元素"""
        startindex=0
        index=3
        result_run = None
        while index<=len(self.nums):
            if self.checkConsecutive(self.nums[startindex:index]):
                    result_run = [i for i in range(startindex,index)]
                    if index-startindex==4:
                        
                        break
                    index+=1
            else:
                startindex+=1
                index+=1
                
        return result_run
    
    
    # def find_nextcard(self,suit,value,cards:list[Card]):
    #     for card in cards:
    #         if card.value == value :
    #             continue
    #         elif card.value == value +1 :
    #             if card.suit == suit:
                    
    #     pass       
    def checkConsecutive(self,cards_value:list[int]) ->bool:
        ##ace can be 1 or 14
        if len(set(cards_value))!=len(cards_value):
            return False
        n = len(cards_value) - 1
        if 14 in cards_value:
            newcards_value=[]
            for value in cards_value:
                if value==14:
                    newcards_value.append(1)
                else:
                    newcards_value.append(value)
            
            return (sum(np.diff(cards_value) == 1) >= n) or (sum(np.diff(sorted(newcards_value)) == 1) >= n)

        return (sum(np.diff(cards_value) == 1) >= n)       

def deal_cards(deck:Deck,playerlist:list[Player],is_show:bool=True):
    for player in playerlist:
        card=deck.deal()
        card.show=is_show
        player.cards.append(card)
    
def refresh_screen(deck:Deck,
                   playerlist:list[Player],
                   board:PlayBoard,
                   round:int,
                   ):
    
    os.system("cls")
    print(f"Round {round}")
    print(deck)
    for player in playerlist:
        print("-"*40)
        print(player)
    # print("-"*40)
    # print(playerlist[0])
    # print("-"*40)
    # print(playerlist[1])
    print("-"*40)
    print(board)    
    print(f"Your point is {str(playerlist[-1].point)}")

def show_hand(player:Player):
    print(("-"*40))
    print(f"{player.name} hand is {player.cards[0].symbol}")

def play_menu():
    print("-"*40)
    print("1.Show you hand")
    print("2.Add 10 point")
    print("3.Pass")
    print("4.All in !!!!!!")
    
def one_vs_one():
    deck=Deck()
    
    computer=Player(name="Computer")
    player=Player()
    playerlist=[computer,player]
    board=PlayBoard(playerlist)
    round=1

    

    while player.point>0 and player.point<200:
        round=1
        deck.shuffle()
        board.reset()
        board.init_point()
        is_allin=False
   
        while round<5:
            
            if round==1:
                deal_cards(deck,playerlist,is_show=False)
                deal_cards(deck,playerlist)
            else:
                deal_cards(deck,playerlist)
            
            #if is_allin is False:
            
                

            

            if is_allin is False:
                refresh_screen(deck,playerlist,board,round)

                while True:
                    play_menu()
                    print("-"*40)
                    choice=input("Your choice is ")
                    """
                    1.Show you hand
                    2.Add 10 point
                    3.Pass
                    4.ShowHand !!
                    
                    
                    """
                    if choice == "1":
                        os.system('cls')
                        refresh_screen(deck,playerlist,board,round)
                        show_hand(player)

                    elif choice == "2":
                        if player.point == 0:
                            print("You point is 0 now !")
                        else:
                            board.point+=10
                            player.point-=10
                            break

                    elif choice == "3":
                        os.system('cls')
                        refresh_screen(deck,playerlist,board,round)
                        break

                    elif choice == "4":
                        if player.point == 0:
                            print("you point is 0 now !")
                        else:
                            board.point+=player.point
                            player.point=0
                            
                            is_allin=True
                            break

                    else:
                        os.system('cls')
                        refresh_screen(deck,playerlist,board,round)
                        print("-"*40)
                        print("Please input valid number!!")


            round+=1
        os.system('cls')
        print("This Turn Result :")
        find_winner(playerlist,board)
        print(board)
        print(f"Your point is {player.point}")
        print("-"*40)
        
        next_turn=True
        if player.point==0:
            print("Game Over You Lose")
            next_turn=False
            
        elif player.point>=200:
            print("Congratulations You Win This Game !!")
            next_turn=False

        
        if next_turn:
            while True:
                
                print("Ready for Next Turn? y/n (n->quit game)")
                print("-"*40)
                wait=input()
                if wait=="n":
                    next_turn=False
                    break
                elif wait=="y":
                    break

                print(f"Your point is {player.point}")
                print("-"*40)
        
        if next_turn is False:
            break

        for player in playerlist:

            player.reset_cards()
        deck.reset()

def find_winner(playerlist:list[Player],board:PlayBoard)->Player:
    ranklist:list[tuple[Player,Any]]=[]
    for player in playerlist:
        player.cards[0].show=True
        player.cards=player.sortedcards()
        score=PokerScore(player.cards)
        rank=score.get_score()
        player.category=score.category
        ranklist.append((player,rank))
    fin_rank=sorted(ranklist,key=lambda x:x[1])
    print(fin_rank)
    winner=fin_rank[-1][0]
    winner.point+=board.point*2
    print("-"*40)
    for player_rank in fin_rank:
        print(f"{player_rank[0]} \nWhich is {player_rank[0].category}")
        #rank[0].point-=10
        #print(rank[0].final_cat)
    print(f"This Turn Winner is {winner.name}")
    print("-"*40)

    return winner
 
def find_winner_simple(playerlist:list[Player])->tuple[Player,list[tuple[Player,Any]]]:
    ranklist:list[tuple[Player,Any]]=[]
    for player in playerlist:
        player.cards[0].show=True
        player.sortedcards()
        score=PokerScore(player.cards)
        rank=score.get_score()
        player.category=score.category
        ranklist.append((player,rank))
    fin_rank=sorted(ranklist,key=lambda x:x[1])
    winner=fin_rank[-1][0]
    # for player_rank in fin_rank:
    #     print(f"{player_rank[0]} \nWhich is {player_rank[0].category}")
    #print(f"This Turn Winner is {winner.name}")

    return winner,fin_rank

def main():



    deck=Deck()
    deck.shuffle()

    handcost=5
    playerlist=[Player() for i in range(5)]
    print(deck)
    for i in range(5):
        deal_cards(deck,playerlist=playerlist)

    ranklist=[]
    for player in playerlist:
        score=PokerScore(player.cards)
        print(player)
        rank=score.get_score()
        ranklist.append((player,rank))
    winner=sorted(ranklist,key=lambda x:x[1])[-1][0]
    print(f"winner {winner}")

    print(deck)


#core algorithm for poker hand evaluation
def poker(hands):
    scores = [(i, score(hand.split())) for i, hand in enumerate(hands)]
    winner = sorted(scores , key=lambda x:x[1])[-1][0]
    return hands[winner]

def score(hand):
    ranks = '23456789TJQKA'
    print({ranks.find(r): ''.join(hand).count(r) for r, _ in hand})
    rcounts = {ranks.find(r): ''.join(hand).count(r) for r, _ in hand}.items()
    score, ranks = zip(*sorted((cnt, rank) for rank, cnt in rcounts)[::-1])
    if len(score) == 5:
        if ranks[0:2] == (12, 3): #adjust if 5 high straight
            ranks = (3, 2, 1, 0, -1)
        straight = ranks[0] - ranks[4] == 4
        flush = len({suit for _, suit in hand}) == 1
        '''no pair, straight, flush, or straight flush'''
        #score = ([1, (3,1,1,1)], [(3,1,1,2), (5,)])[flush][straight]
        score = ([(1, ), (3,1,1,1)], [(3,1,1,2), (5,)])[flush][straight]
    return score, ranks

def random_generate_card() ->Card:
    """random generate one Card obj"""
    
    suits={'hearts':"♡",'diamonds':"♢",'spades':"♠",'clubs':"♣"}
    values={
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5,
        "Six":6,
        "Seven":7,
        "Eight":8,
        "Nive":9,
        "Ten":10,
        "Jack":11,
        "Queen":12,
        "King":13,
        "Ace":14,
    }                        
    suit = random.choice(list(suits.keys()))
    name = random.choice(list(values.keys()))
    value = values[name]
    symbol = suits[suit]
    if value>10:
        symbol=name[0]+symbol
    else:
        symbol=str(value)+symbol
    
    card=Card(suit,value,name,symbol)
    # if random.randint(0,1):
    #     card.show=False
    return card


def generate_run() -> list[Card]:
    cards=[]
    for name in list(VALUES)[:4]:
        value = value=VALUES[name]
        suit = list(SUITS.keys())[0]
        symbol = SUITS[suit]
        if value>10:
            symbol=name[0]+symbol
        else:
            symbol=str(value)+symbol
        card = Card(suit,name=name,value=value,symbol=symbol)
        cards.append(card)
    
    return cards   
    

#*********************************
#core algorithm for blackjack game
#*********************************

#calculate the cardpoint for backjack game               
def cal_blackjack(player:Player) -> None:
    total_point=0
    player_has_A=False
    for card in player.cards:
        if card.value<=10:
            total_point+=card.value
        elif 10<card.value<=13:
            total_point+=10
        else:
            total_point+=1
            player_has_A=True
    
    if player_has_A and total_point+10<=21:
        total_point+=10
    player.blackjack_point=total_point       

#compare with two player point and return winner               
def find_blackjack_winner(computer:Player,player:Player)->Optional[Player]:
    if player.blackjack_point>21:
        return computer
        
    elif computer.blackjack_point>21:
        return player
        
    elif computer.blackjack_point>player.blackjack_point:
        return computer
        
    elif computer.blackjack_point<player.blackjack_point:
        return player
    else:
        return None 
            





          
if __name__ == "__main__":


    #main()
    #one_vs_one()
    
    
    a=Player()
    #card=random_generate_card()
    for _ in range(10):
        a.cards.append(random_generate_card())
    a.cards=generate_run()
    a.sortedcards_by_num()
    print(a)
    for card in a.cards:
        print(card.num)
    test = RummyAI(hands=a.cards)
    print(test.has_run())
    
    


    #card=Card(suit='hearts',value=14),
    # a=[(2, 4), (1, 14), (1, 8), (1, 5)]
    # b=[(2, 6), (1, 14), (1, 8), (1, 5)]
    # c=[(2, 9), (1, 14), (1, 8), (1, 5)]
    # f=[(1, 9), (1, 14), (1, 8), (1, 5),(1, 2)]
    # d=[a,c,b,f]
    # print(sorted(d))

    # deck=Deck()
    # # for i in range(5):
    # #     print(random.choices(deck.deck,k=5))
    # deck.shuffle()
    # player_1=Player()

    # testcards=[
    #     Card(suit='hearts',value=14),
    #     Card(suit='hearts',value=2),
    #     Card(suit='hearts',value=3),
    #     Card(suit='spades',value=4),
    #     Card(suit='diamonds',value=5),

        
    # ]
    # player_1.cards=testcards
    # score=PokerScore(testcards)
    # score.get_score




    # for i in range(5):
    #     card=deck.deal()
    #     card.show=True
    #     player_1.cards.append(card)
    # player_1.cal_values()
    # print(player_1.cards)
    # print(player_1.sortedcards())
    # print(player_1.cards)
    #print(player_1.straight())
    #print(player_1.highcardvalue())
    




    #print(f"deck remain {deck.num_of_crads()}")
    #print(f'my cards is {mycards}')

    