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
        
        
        
if __name__ == "__main__":
    unittest.main()