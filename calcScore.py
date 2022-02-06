# see https://puyobites.com/posts/puyo_damage/
# see https://www.bilibili.com/read/cv6802681
# Score = (10 * NumPopped) * (ChainPower + ColorBonus + GroupBonus)
import math

"""计算消除的分数"""
def getGroupBounds(numInGroup):
    bonus = 0
    if numInGroup == 4:
        bonus = 0
    elif numInGroup >= 5 and numInGroup <= 10:
        bonus = numInGroup-3
    elif numInGroup > 10:
        bonus = 10
    return bonus


def getChainPower(chainNum):
    p = 0
    if chainNum == 1:
        p = 0
    elif chainNum >= 2 and chainNum <= 5:
        p = math.pow(2, chainNum+1)
    elif chainNum > 5:
        p = 64 + (chainNum-5)*32
    return p


def getColorBonus(colorNum):
    b = 0
    if colorNum == 1:
        b = 0
    elif colorNum == 2:
        b = 3
    elif colorNum == 3:
        b = 6
    elif colorNum == 4:
        b = 12
    elif colorNum == 5:
        b = 24
    return b


def calcScore(chainNum, links):
    """计算分数"""
    # 消除的总数
    numPopped = 0
    chainPower = getChainPower(chainNum)

    totalGroupBonus = 0

    # 每个颜色放到此数组中
    colors = []
    for link in links:
        cell0 = link[0]
        color = cell0.color

        if not color in colors:
            colors.append(color)
        groupBonus = getGroupBounds(len(link))
        totalGroupBonus += groupBonus
        numPopped += len(link)
    colorBonus = getColorBonus(len(colors))
    score = (10*numPopped)*max((chainPower+colorBonus+totalGroupBonus), 1)
    return int(score)

# Score = (10 * NumPopped) * (ChainPower + ColorBonus + GroupBonus)


class FCell:
    def __init__(self, color):
        self.color = color


# https://puyonexus.com/chainsim/chain/wHyK5
    # （8*10）* max(（0+0+0）,1) = 80
links = [
    (FCell("R"), FCell("R"), FCell("R"), FCell("R")),
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"))
]
score = calcScore(1, links)
# print(score)
# https://puyonexus.com/chainsim/chain/DrbEq
# (8*10)* (0+0+5)=400
links = [
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"),
     FCell("R"), FCell("R"), FCell("R"), FCell("R"))
]
score = calcScore(1, links)
# print(score)
# https://puyonexus.com/chainsim/chain/ZoBeo
# (10*10)*(0+0+(2+2))=400
links = [
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"), FCell("R")),
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"), FCell("R"))
]
score = calcScore(1, links)
# print(score)
# https://puyonexus.com/chainsim/chain/8vFYj
# (10*10)*(0+0+7)=700
links = [
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"), FCell("R"), FCell("R"),
     FCell("R"), FCell("R"), FCell("R"), FCell("R"))
]
score = calcScore(1, links)
# print(score)
# 4*6 chain
# https://puyonexus.com/chainsim/chain/DneJC
links = [
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"))
]
score = 0
for i in range(1, 7):
    s = calcScore(i, links)
    # print(str(i), ":", str(s))
    score += s
# print(score)

# 5*6 chain
# https://puyonexus.com/chainsim/chain/BZ5QF
links = [
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"), FCell("R"))
]
score = 0
for i in range(1, 7):
    s = calcScore(i, links)
    # print(str(i), ":", str(s))
    score += s
# print(score)

# tow color
# https://puyonexus.com/chainsim/chain/v5otp
links = [
    (FCell("R"), FCell("R"), FCell("R"), FCell("R"), FCell("R")),
    (FCell("G"), FCell("G"), FCell("G"), FCell("G"), FCell("G"))
]
score = calcScore(1, links)
# print(score)