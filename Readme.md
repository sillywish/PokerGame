# Pokergame
## deverlopment log
## 2023 10/12 
修改PlayerFrame 添加了生成复杂手牌的功能，优化了之前的功能函数
生成CardLabel和CardState类 完成纸牌的一些事件操作
## 2023 10/13
完成了打出牌所需要的函数操作
添加了FRAMESIZE类，能更好的统一改变修改PlayerFrame的大小
修改了卡牌排序的方式 改为冒泡排序
## 2023 10/14
添加了DeckFrame 内置抽牌堆和弃牌堆
实现了PlayerFrame 与 DeckFrame 的连接
完成了玩家从抽牌堆和弃牌堆抽牌的功能
完成了玩家弃牌到弃牌堆的功能
## 2023 10/16 
实现了同花顺和3对以上的判断
构建了基本UI界面
## 2023 10/19
实现了rummy layout逻辑的基本判断
实现了rummy ui layout按钮的基本功能
实现了computer 对弃牌堆卡的判断
## 2023 10/20
实现了computer 对layout牌堆的判断
完成简单电脑游玩AI逻辑的编写
修改了一些逻辑性的BUG
实现一局完整的简单对局
## 2023 10/23
添加对MELD时的判断
添加电脑AI的弃牌逻辑 计算每张卡牌的COST COST算法如下
### cost for rummy cards
    cost=base point + set point +run point
    basepoint: 1-10 point, the more value the less point value >=10 point =1
    setpoint : has same set cards  10 point
    runpoint : etc (9,10)pair 20 point , etc (7,9) 10 point 
修改CARD的symbol为property
## 2023 10/24
添加了message_frame 用于展示游戏内的消息
tkinter 没有自带滚动条的Frame 因此创建了AutoScrollbar,AutoScrollbarAPP
将meld_frame 修改为AutoScrollbarAPP类
修改了一些COST的计算 对边缘的卡A K 减少权重uni
添加了unittest.py 用于测试
## 2023 10/25
优化了rummy 全部和判断run有关的算法 不使用numpy.diff
重写了判断是否从弃牌抽牌的函数 优化了性能
完成了游戏的重新开始功能
添加rummystate.INIT 状态 用于游戏开始的初始化
整合了PlayerFrame label 和 player 的reset 函数
整合了DeckFrame 相关reset操作 为reset_deck 函数
添加了统计分数的规则
## 2023 10/26

！！！！！！！！！有时玩家丢弃卡牌 电脑又可以组成meld时 会出现BUG 还在排查