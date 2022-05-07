# bullet.py - 敵弾
#


# 参照
#
import pyxel
import random
from system.draw import Draw
from const import Const
from actor import Actor
from manager import Manager
from collision import Collision
from xyz import Xyz
from player import Player


# 敵弾クラス
#
class Bullet(Actor):

    # 位置
    __POSITION_X_MIN    = Xyz.X_MIN - 8
    __POSITION_X_MAX    = Xyz.X_MAX + 8
    __POSITION_Y_MIN    = Xyz.Y_MIN - 8
    __POSITION_Y_MAX    = Xyz.Y_MAX + 8

    # 矩形
    __RECTS = [
        [-2, -2,  1,  1, ], 
        [-3, -3,  2,  2, ], 
        [-5, -5,  4,  4, ], 
        [-7, -7,  6,  6, ], 
    ]

    # イメージ
    __IMAGE_U   = 0
    __IMAGE_V   = 32
    __IMAGE_W   = 16
    __IMAGE_H   = 16
    __IMAGE_X   = -8
    __IMAGE_Y   = -8

    # コンストラクタ
    def __init__(self, manager, x, y, z):

        # マネージャの取得
        self.__manager = manager

        # 描画の取得
        self.__draw = Draw.get_instance()

        # ライフの初期化
        self.__life = 1

        # ダメージの初期化
        self.__damage = 0

        # 位置の初期化
        self.__position_x = x
        self.__position_y = y
        self.__position_z = z

        # 速度の初期化
        self.__speed_x = 0
        self.__speed_y = 0
        self.__speed_z = 0.5

        # 画面位置の初期化
        self.__screen_x = 0
        self.__screen_y = 0
        self.__screen_scale = 0

        # コリジョンの初期化
        self.__collision = Collision()

        # アニメーションの初期化
        self.__animation = 0

        # 処理の初期化
        self.__process = self.shoot
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # ライフの更新
        if self.__process is not None:
            if self.__damage > 0:
                self.__life = max(self.__life - self.__damage, 0)
                self.__damage = 0
                if self.__life == 0:
                    self.delete()

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

        # 弾の描画
        pyxel.blt(
            self.__screen_x + Bullet.__IMAGE_X + Xyz.O_X, 
            self.__screen_y + Bullet.__IMAGE_Y + Xyz.O_Y, 
            0, 
            Bullet.__IMAGE_U + (((self.__animation >> 1) & 0x01) * 4 + self.__screen_scale) * Bullet.__IMAGE_W, 
            Bullet.__IMAGE_V, 
            Bullet.__IMAGE_W, 
            Bullet.__IMAGE_H, 
            pyxel.COLOR_BLACK
        )

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # 敵弾を破棄する
    def delete(self):

        # 敵弾の破棄
        self.__manager.delete(self)
        self.__process = None

    # 敵弾を撃つ
    def shoot(self):

        # 初期化
        if self.__state == 0:

            # 速度の設定
            player = self.__manager.get_actors(Player)
            if player:
                p = player[0].get_position()
                if p is not None:
                    px = p[0] + random.randint(-12, 11)
                    py = p[1] + random.randint(-8, 7)
                    self.__speed_x = min(max((self.__position_x - px) / (self.__position_z / self.__speed_z), -3), 3)
                    self.__speed_y = min(max((self.__position_y - py) / (self.__position_z / self.__speed_z), -3), 3)

            # 初期化の完了
            self.__state = self.__state + 1
        
        # 移動
        self.__position_x = self.__position_x + self.__speed_x
        self.__position_y = self.__position_y + self.__speed_y
        self.__position_z = self.__position_z + self.__speed_z

        # 移動の完了
        if self.__position_z > Xyz.Z_NEAR or self.__position_x < Bullet.__POSITION_X_MIN or self.__position_x >= Bullet.__POSITION_X_MAX or self.__position_y < Bullet.__POSITION_Y_MIN or self.__position_y >= Bullet.__POSITION_Y_MAX:
            self.delete()

        # アニメーションの更新
        self.__animation = self.__animation + 1

    # 座標情報を計算する
    def calc(self):

        # 画面位置の設定
        screen = Xyz.calc(int(self.__position_x), int(self.__position_y), int(self.__position_z))
        self.__screen_x = screen[0]
        self.__screen_y = screen[1]
        self.__screen_scale = screen[2]

        # コリジョンの設定
        self.__collision.set(
            left   = self.__screen_x + Bullet.__RECTS[self.__screen_scale][0], 
            top    = self.__screen_y + Bullet.__RECTS[self.__screen_scale][1], 
            right  = self.__screen_x + Bullet.__RECTS[self.__screen_scale][2], 
            bottom = self.__screen_y + Bullet.__RECTS[self.__screen_scale][3], 
            z      = self.__position_z
        )

    # ヒット判定を行う
    def hit(self, target):

        # ヒットの判定
        return self.__process is not None and self.__life > self.__damage and self.__collision.hit(target)

    # ダメージを食らう
    def damage(self):

        # ダメージの更新
        self.__damage = self.__damage + 1

        # サウンドの再生
        pyxel.play(3, Const.SOUND_HIT)
        
    # レポートする
    def report(self):

        # レポートなし
        return 0
