# bomb.py - 爆発
#


# 参照
#
import pyxel
from system.draw import Draw
from const import Const
from actor import Actor
from manager import Manager
from xyz import Xyz


# 爆発クラス
#
class Bomb(Actor):

    # イメージ
    __IMAGE_U   = 64
    __IMAGE_V   = 16
    __IMAGE_W   = 16
    __IMAGE_H   = 16
    __IMAGE_X   = -8
    __IMAGE_Y   = -8

    # コンストラクタ
    def __init__(self, manager, x, y, z, frame):

        # マネージャの取得
        self.__manager = manager

        # 描画の取得
        self.__draw = Draw.get_instance()

        # 位置の初期化
        self.__position_x = x
        self.__position_y = y
        self.__position_z = z

        # 画面位置の初期化
        self.__screen_x = 0
        self.__screen_y = 0
        self.__screen_scale = 0

        # アニメーションの初期化
        self.__animation = frame
        
        # 処理の初期化
        self.__process = None
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # 初期化
        if self.__state == 0:

            # サウンドの再生
            pyxel.play(3, Const.SOUND_BOMB)
            
            # 初期化の完了
            self.__state = self.__state + 1

        # アニメーションの更新
        self.__animation = self.__animation - 1

        # アニメーションの継続
        if self.__animation > 0:

            # 画面位置の更新
            self.calc()

            # 描画の追加
            self.__draw.append(self.__position_z, self.draw)

        # アニメーションの完了
        else:
            self.__manager.delete(self)

    # フレーム毎の描画を行う
    def draw(self):

        # 爆発の描画
        pyxel.blt(
            self.__screen_x + Bomb.__IMAGE_X + Xyz.O_X, 
            self.__screen_y + Bomb.__IMAGE_Y + Xyz.O_Y, 
            0, 
            Bomb.__IMAGE_U + self.__screen_scale * Bomb.__IMAGE_W, 
            Bomb.__IMAGE_V, 
            Bomb.__IMAGE_W * ((self.__animation & 0x04) / 2 - 1), 
            Bomb.__IMAGE_H, 
            pyxel.COLOR_BLACK
        )

    # 座標情報を計算する
    def calc(self):

        # 画面位置の設定
        screen = Xyz.calc(self.__position_x, self.__position_y, self.__position_z)
        self.__screen_x = screen[0]
        self.__screen_y = screen[1]
        self.__screen_scale = screen[2]

    # レポートする
    def report(self):

        # レポートなし
        return 0
