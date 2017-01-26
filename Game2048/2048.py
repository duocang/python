#-*coding UTF-8 -*-
import curses
from random import randrange, choice
from collections import defaultdict

# 用户行为
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']

# 阻塞+循环，直到获得用户的有效输入才返回对应行为
def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

#矩阵转置
def transpose(field):
    return [list(row) for row in zip(*field)]

#矩阵逆转，不是逆矩阵
def invert(field):
    return [row[::-1] for row in field]

#初始化棋盘参数，可以指定棋盘的高度和宽度以及游戏胜利的调教
class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height=height
        self.width = width
        self.win_value = 2048
        self.score = 0
        self.highscore = 0
        self.reset(self)

    #重置棋盘
    def reset(self):
        if self.score > self.highscore:
            self.height = self.score
        self.score = 0;
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    #通过对矩阵进行转置与逆转，可以直接从左移得到其余三个方向的移动操作
    def move(self, direction):
        #一行向左合并
        def move_row_left(row):
            def tighten(row):#把零散的非零单元挤到一块
                new_row = [i for i in row if i != 0]#剔除0元素
                new_row += [0 for i in range(len(row) - len(new_row))]#在末尾添加0元素
                return new_row

            def merge(row):# 对邻近元素进行合并
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i+1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            #先挤到一起再合并再挤到一起
            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False


#随机生成一个2或4
def spawn(self):
    new_element = 4 if randrange(100) > 89 else 2
    (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.width) for j in range(self.height) if self.field[i][j] ==0])
    self.field[i][j] = new_element


#重置棋盘
def reset(self):

#一行向左合并

#


#有效输入键是最常见的 W（上），A（左），S（下），D（右），R（重置），Q（退出）,
# 这里要考虑到大写键开启的情况，获得有效键值列表：
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']

#将输入与行为进行关联：
actions_dict = dict(zip(letter_codes, actions * 2))

#state存储当前状态，state_actions这次词典变量作为状态转换的规则，它的key是状态，
#value是返回下一个状态的函数：


def main(stdscr):
    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'

    def not_game(state):
        #画出GameOver或者Win的界面
        responses = defaultdict(lambda:state) #默认是当前状态，没有行为就会一直在当前界面循环
        responses['Restart'], responses['Exit'] = 'Init', 'Exit' #对应不同的行为转换到不同状态
        return responses[action]

    def game():
        #画出当前棋盘状态
        #读取用户当前输入action
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        #if 成功移动一步

