# enemy_pole.py - 柱
#


# 参照
#
import pyxel
import random
from system.draw import Draw
from enemy import Enemy
from collision import Collision
from xyz import Xyz


# 柱クラス
#
class EnemyPole(Enemy):

    # 矩形
    __RECTS = [
        [-2,  0,  1,  0, ], 
        [-3,  0,  2,  0, ], 
        [-7,  0,  6,  0, ], 
        [-9,  0,  8,  0, ], 
    ]

    # イメージ
    __IMAGE_U           = 0
    __IMAGE_V_TOP       = 112
    __IMAGE_V_MIDDLE    = 120
    __IMAGE_V_BOTTOM    = 128
    __IMAGE_W           = 24
    __IMAGE_H           = 8
    __IMAGE_X           = -12
    __IMAGE_Y           = 0

    # コンストラクタ
    def __init__(self, manager, level):

        # マネージャの取得
        self.__manager = manager

        # 描画の取得
        self.__draw = Draw.get_instance()

        # 位置の初期化
        self.__position_x = random.randint(-3, 3) * 22
        self.__position_y = Xyz.Y_MAX
        self.__position_z = Xyz.Z_FAR

        # 画面位置の初期化
        self.__screen_x = 0
        self.__screen_y = 0
        self.__screen_scale = 0
        self.__screen_height = 0

        # コリジョンの初期化
        self.__collision = Collision()

        # 処理の初期化
        self.__process = self.approach
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # 処理の実行
        if self.__process is not None:
            self.__process()

        # 画面位置の更新
        if self.__process is not None:
            self.calc()

        # 描画の追加
        if self.__process is not None:
            self.__draw.append(self.__position_z, self.draw)

    # フレーム毎の描画を行う
    def draw(self):

        # 柱の描画
        x = self.__screen_x + EnemyPole.__IMAGE_X + Xyz.O_X
        y = self.__screen_y + Xyz.O_Y
        u = EnemyPole.__IMAGE_U + self.__screen_scale * EnemyPole.__IMAGE_W
        h = self.__screen_height
        pyxel.blt(x, y, 0, u, EnemyPole.__IMAGE_V_BOTTOM, EnemyPole.__IMAGE_W, EnemyPole.__IMAGE_H, pyxel.COLOR_BLACK)
        while h >= EnemyPole.__IMAGE_H:
            y = y - EnemyPole.__IMAGE_H
            h = h - EnemyPole.__IMAGE_H
            pyxel.blt(x, y, 0, u, EnemyPole.__IMAGE_V_MIDDLE, EnemyPole.__IMAGE_W, EnemyPole.__IMAGE_H, pyxel.COLOR_BLACK)
        if h > 0:
            y = y - h
            pyxel.blt(x, y, 0, u, EnemyPole.__IMAGE_V_MIDDLE, EnemyPole.__IMAGE_W, h, pyxel.COLOR_BLACK)
        y = y - EnemyPole.__IMAGE_H
        pyxel.blt(x, y, 0, u, EnemyPole.__IMAGE_V_TOP, EnemyPole.__IMAGE_W, EnemyPole.__IMAGE_H, pyxel.COLOR_BLACK)

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # 柱を破棄する
    def delete(self):

        # 示談の破棄
        self.__manager.delete(self)
        self.__process = None

    # 柱が接近する
    def approach(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1

        # 移動
        self.__position_z = self.__position_z + 0.5

        # 移動の完了
        if self.__position_z > Xyz.Z_NEAR:
            self.delete()

    # 座標情報を計算する
    def calc(self):

        # 画面位置の設定
        screen = Xyz.calc(self.__position_x, self.__position_y, self.__position_z)
        self.__screen_x = screen[0]
        self.__screen_y = screen[1]
        self.__screen_scale = screen[2]
        self.__screen_height = screen[3]

        # コリジョンの設定
        self.__collision.set(
            left   = self.__screen_x + EnemyPole.__RECTS[self.__screen_scale][0], 
            top    = self.__screen_y - self.__screen_height, 
            right  = self.__screen_x + EnemyPole.__RECTS[self.__screen_scale][2], 
            bottom = self.__screen_y, 
            z      = self.__position_z
        )

    # ヒット判定を行う
    def hit(self, target):

        # ヒットの判定
        return Enemy.HIT_NOEFFECT if self.__process is not None and self.__collision.hit(target) else Enemy.HIT_NONE

    # ダメージを食らう
    def damage(self):
        pass

    # レポートを返す
    def report(self):

        # レポートなし
        return 0