screenWidth = 1280
screenHeight = 750
#游戏版的宽度有6个格子
BOARD_COL = 6
#游戏版的高度有12个格子
BOARD_ROW = 12
#每个格子32个像素
# CELL_SIZE=72
CELL_SIZE=50
TXT_R = "R"
TXT_G = "G"
TXT_B = "B"
TXT_P = "P"
TXT_Y = "Y"
TXT_COLORS = [TXT_R,  TXT_G,  TXT_B,  TXT_P,  TXT_Y]
RGB_R = (255, 0, 0)
RGB_G = (0, 255, 0)
RGB_B = (0, 0, 255)
RGB_P = (255, 0, 255)
RGB_Y = (255, 255, 0)
RGB_COLORS = [RGB_R, RGB_G,RGB_B, RGB_P,RGB_Y]
#用户控制时，使用多少帧走一个格子，越大越慢
FRAME_PER_CELL_CONTROLL = 3
#向下跌落时，使用多少帧走一个格子，越大越慢
FRAME_PER_CELL_FALLDOWN = 3

#不受控制，自动下落时，每隔多少帧下降一个格子，越大越慢
FRAME_FREEDOWN = 60