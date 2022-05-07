# shot.py - 自弾
#


# 参照
#
import pyxel
from system.draw import Draw
from const import Const
from actor import Actor
from manager import Manager
from collision import Collision
from xyz import Xyz


# 自弾クラス
#
class Shot(Actor):

    # 位置
    __POSITION_X_MIN    = Xyz.X_MIN - 8
    __POSITION_X_MAX    = Xyz.X_MAX + 8
    __POSITION_Y_MIN    = Xyz.Y_MIN - 8
    __POSITION_Y_MAX    = Xyz.Y_MAX + 8

    # 速度
    __SPEED_SHOOT_X     = 0
    __SPEED_SHOOT_Y     = 0
    __SPEED_SHOOT_Z     = -1
    __SPEED_REBOUND_X   = 4
    __SPEED_REBOUND_Y   = 2
    __SPEED_REBOUND_Z   = 0

    # 矩形
    __RECTS = [
        [-2, -2,  1,  1, ], 
        [-3, -3,  2,  2, ], 
        [-5, -5,  4,  4, ], 
        [-7, -7,  6,  6, ], 
    ]

    # イメージ
    __IMAGE_U   = 0
    __IMAGE_V   = 16
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
        self.__speed_x = Shot.__SPEED_SHOOT_X
        self.__speed_y = Shot.__SPEED_SHOOT_Y
        self.__speed_z = Shot.__SPEED_SHOOT_Z

        # 画面位置の初期化
        self.__screen_x = 0
        self.__screen_y = 0
        self.__screen_scale = 0

        # コリジョンの初期化
        self.__collision = Collision()

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
            self.__screen_x + Shot.__IMAGE_X + Xyz.O_X, 
            self.__screen_y + Shot.__IMAGE_Y + Xyz.O_Y, 
            0, 
            Shot.__IMAGE_U + self.__screen_scale * Shot.__IMAGE_W, 
            Shot.__IMAGE_V, 
            Shot.__IMAGE_W, 
            Shot.__IMAGE_H, 
            pyxel.COLOR_BLACK
        )

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # 自弾を破棄する
    def delete(self):

        # 自弾の破棄
        self.__manager.delete(self)
        self.__process = None

    # 自弾を撃つ
    def shoot(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1
        
        # 移動
        self.__position_x = self.__position_x + self.__speed_x
        self.__position_y = self.__position_y + self.__speed_y
        self.__position_z = self.__position_z + self.__speed_z

        # 移動の完了
        if self.__position_z < Xyz.Z_FAR or self.__position_x < Shot.__POSITION_X_MIN or self.__position_x >= Shot.__POSITION_X_MAX or self.__position_y < Shot.__POSITION_Y_MIN or self.__position_y >= Shot.__POSITION_Y_MAX:
            self.delete()

    # 座標情報を計算する
    def calc(self):

        # 画面位置の設定
        screen = Xyz.calc(self.__position_x, self.__position_y, self.__position_z)
        self.__screen_x = self.__position_x
        self.__screen_y = screen[1]
        self.__screen_scale = screen[2]

        # コリジョンの設定
        self.__collision.set(
            left   = self.__screen_x + Shot.__RECTS[self.__screen_scale][0], 
            top    = self.__screen_y + Shot.__RECTS[self.__screen_scale][1], 
            right  = self.__screen_x + Shot.__RECTS[self.__screen_scale][2], 
            bottom = self.__screen_y + Shot.__RECTS[self.__screen_scale][3], 
            z      = self.__position_z
        )

    # コリジョンを取得する
    def get_collision(self):

        # コリジョンの取得
        return self.__collision if self.__process is not None and self.__life > self.__damage else None

    # ダメージを食らう
    def damage(self):

        # ダメージの更新
        self.__damage = self.__damage + 1

        # サウンドの再生
        # pyxel.play(3, Const.SOUND_HIT)
        
    # リバウンドさせる
    def rebound(self):

        # 速度の設定
        self.__speed_x = Shot.__SPEED_REBOUND_X if self.__position_x >= 0 else -Shot.__SPEED_REBOUND_X
        self.__speed_y = Shot.__SPEED_REBOUND_Y if self.__position_y >= 0 else -Shot.__SPEED_REBOUND_Y
        self.__speed_z = Shot.__SPEED_REBOUND_Z

        # ライフの減少
        self.__life = 0

        # サウンドの再生
        pyxel.play(3, Const.SOUND_NOEFFECT)

    # レポートを返す
    def report(self):

        # レポートなし
        return 0
    