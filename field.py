# field.py - フィールド
#


# 参照
#
import pyxel
from system.draw import Draw
from manager import Manager
from actor import Actor


# フィールドクラス
#
class Field(Actor):

    # 遠景
    __FAR_IMAGE_U   = 128
    __FAR_IMAGE_V   = 0
    __FAR_IMAGE_W   = 128
    __FAR_IMAGE_H   = 48
    __FAR_IMAGE_X   = 0
    __FAR_IMAGE_Y   = 0

    # 地面
    __GROUNDS = [
        0b000000001111110000111001, 
        0b000000011111110000111001, 
        0b000000111111100001111001, 
        0b000001111111000001110001, 
        0b000011111111000011110011, 
        0b000111111110000011110011, 
        0b001111111100000111100011, 
        0b011111111000000111100011, 
    ]
    __GROUND_FRAME_LENGTH   = 2
    __GROUND_HEIGHT         = 24
    __GROUND_IMAGE_U        = 128
    __GROUND_IMAGE_V        = 48
    __GROUND_IMAGE_W        = 128
    __GROUND_IMAGE_H        = 1
    __GROUND_IMAGE_X        = 0
    __GROUND_IMAGE_Y        = 48

    # コンストラクタ
    def __init__(self, manager):

        # マネージャの取得
        self.__manager = manager

        # 描画の取得
        self.__draw = Draw.get_instance()

        # 地面の初期化
        self.__ground_scroll = 0
        self.__ground_frame = 0

        # 処理の初期化
        self.__process = None
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1

        # 地面の更新
        self.__ground_frame = self.__ground_frame + 1
        if self.__ground_frame >= Field.__GROUND_FRAME_LENGTH:
            self.__ground_scroll = self.__ground_scroll + 1
            self.__ground_frame = 0

        # 描画の追加
        self.__draw.append(-10000, self.draw)

    # フレーム毎の描画を行う
    def draw(self):

        # 遠景の描画
        pyxel.blt(Field.__FAR_IMAGE_X, Field.__FAR_IMAGE_Y, 0, Field.__FAR_IMAGE_U, Field.__FAR_IMAGE_V, Field.__FAR_IMAGE_W, Field.__FAR_IMAGE_H)

        # 地面の描画
        mask = Field.__GROUNDS[self.__ground_scroll & 0x07]
        if (self.__ground_scroll & 0x08) != 0:
            mask = ~mask
        for i in range(Field.__GROUND_HEIGHT):
            v = Field.__GROUND_IMAGE_V + i
            if (mask & (1 << i)) != 0:
                v = v + Field.__GROUND_HEIGHT
            pyxel.blt(Field.__GROUND_IMAGE_X, Field.__GROUND_IMAGE_Y + i, 0, Field.__GROUND_IMAGE_U, v, Field.__GROUND_IMAGE_W, Field.__GROUND_IMAGE_H)

    # レポートを返す
    def report(self):

        # レポートなし
        return 0
