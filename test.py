import unittest

from cardgame import *


class TestFunction(unittest.TestCase):
    
    def test_find_layout(self):
        test_list1 = [Card(suit='hearts',value=2,name="Two"),
                      Card(suit='hearts',value=3,name="Three"),
                      Card(suit='hearts',value=4,name="Four"),]
        
        test1_ans = [Card(suit='hearts',value=1,name="Ace"),
                     Card(suit='hearts',value=5,name="Five"),]
        
        self.assertAlmostEqual(find_layout_cards(test_list1),test1_ans)
    
    
    def test_evaluate_discard(self):
        test_list1 = [Card(suit='clubs',value=2,name="Two"),
                      Card(suit='hearts',value=4,name="Four"),
                      Card(suit='hearts',value=2,name="Two"),
                      Card(suit='clubs',value=3,name="Three")]
        
        test_card1 = Card(suit='hearts',value=3,name="Three")
        test_card2 = Card(suit='spades',value=2,name="Two")
        test_card3 = Card(suit='spades',value=6,name="Six")
        
        
        self.assertAlmostEqual(evaluate_discard(test_card1,test_list1),True)
        self.assertAlmostEqual(evaluate_discard(test_card2,test_list1),True)
        self.assertAlmostEqual(evaluate_discard(test_card3,test_list1),False)      
        
        
if __name__ == "__main__":
    unittest.main()