# enemy_julli.py - ジェリィ
#


# 参照
#
import pyxel
import math
import random
from system.draw import Draw
from enemy import Enemy
from collision import Collision
from xyz import Xyz
from bullet import Bullet
from bomb import Bomb


# ジェリィクラス
#
class EnemyJurii(Enemy):

    # 発射
    __FIRE_DISTANCE = -7

    # 矩形
    __RECTS = [
        [ -4,  -3,   4,   2, ], 
        [ -6,  -5,   6,   4, ], 
        [ -9,  -6,   9,   5, ], 
        [-11,  -8,  11,   7, ], 
    ]

    # イメージ
    __IMAGE_U   = 0
    __IMAGE_V   = 80
    __IMAGE_W   = 24
    __IMAGE_H   = 16
    __IMAGE_X   = -12
    __IMAGE_Y   = -8

    # コンストラクタ
    def __init__(self, manager, level):

        # マネージャの取得
        self.__manager = manager

        # 描画の取得
        self.__draw = Draw.get_instance()

        # ライフの初期化
        self.__life = 1

        # ダメージの初期化
        self.__damage = 0

        # 位置の初期化
        self.__position_x = random.randint(-48, 48)
        self.__position_y = Xyz.Y_MAX
        self.__position_z = Xyz.Z_FAR

        # 移動の初期化
        self.__move_count = 0

        # 発射の初期化
        self.__fire = 0
        self.__fire_interval = max(60 - 5 * level, 30)

        # 画面位置の初期化
        self.__screen_x = 0
        self.__screen_y = 0
        self.__screen_scale = 0

        # コリジョンの初期化
        self.__collision = Collision()

        # スコアの初期化
        self.__score = 0

        # 処理の初期化
        self.__process = self.move
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # ライフの更新
        if self.__process is not None:
            if self.__damage > 0:
                self.__life = max(self.__life - self.__damage, 0)
                self.__damage = 0
                if self.__life == 0:
                    self.__manager.append(Bomb(self.__manager, self.__position_x, self.__position_y, self.__position_z, 16))
                    self.__score = 1
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

        # ジェリィの描画
        pyxel.blt(
            self.__screen_x + EnemyJurii.__IMAGE_X + Xyz.O_X, 
            self.__screen_y + EnemyJurii.__IMAGE_Y + Xyz.O_Y, 
            0, 
            EnemyJurii.__IMAGE_U + self.__screen_scale * EnemyJurii.__IMAGE_W, 
            EnemyJurii.__IMAGE_V, 
            EnemyJurii.__IMAGE_W, 
            EnemyJurii.__IMAGE_H, 
            pyxel.COLOR_BLACK
        )

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # ジェリィを破棄する
    def delete(self):

        # 示談の破棄
        self.__manager.delete(self)
        self.__process = None

    # ジェリィが移動する
    def move(self):

        # 初期化
        if self.__state == 0:

            # 発射の設定
            self.__fire = random.randint(self.__fire_interval, self.__fire_interval + 59)

            # 初期化の完了
            self.__state = self.__state + 1

        # 移動
        self.__move_count = self.__move_count + 1
        self.__position_y = Xyz.Y_MAX - 48 * math.sin(((self.__move_count << 2) & 0x7f) * 2 * math.pi / 256)
        self.__position_z = self.__position_z + 0.25

        # 発射
        self.__fire = self.__fire - 1
        if self.__fire == 0:
            if self.__position_z < EnemyJurii.__FIRE_DISTANCE:
                self.__manager.append(Bullet(self.__manager, self.__position_x, self.__position_y, self.__position_z + 1))
            self.__state = 0

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

        # コリジョンの設定
        self.__collision.set(
            left   = self.__screen_x + EnemyJurii.__RECTS[self.__screen_scale][0], 
            top    = self.__screen_y + EnemyJurii.__RECTS[self.__screen_scale][1], 
            right  = self.__screen_x + EnemyJurii.__RECTS[self.__screen_scale][2], 
            bottom = self.__screen_y + EnemyJurii.__RECTS[self.__screen_scale][3], 
            z      = self.__position_z
        )

    # ヒット判定を行う
    def hit(self, target):

        # ヒットの判定
        return Enemy.HIT_DAMAGE if self.__process is not None and self.__life > self.__damage and self.__collision.hit(target) else Enemy.HIT_NONE

    # ダメージを食らう
    def damage(self):

        # ダメージの更新
        self.__damage = self.__damage + 1

    # レポートする
    def report(self):

        # スコアを返す
        return self.__score

