# enemy_julli.py - スタンパロン
#


# 参照
#
import pyxel
import math
import random
from system.draw import Draw
from const import Const
from enemy import Enemy
from collision import Collision
from xyz import Xyz
from bullet import Bullet
from bomb import Bomb


# スタンパロンクラス
#
class EnemyStamperon(Enemy):

    # 位置
    __POSITION_X_MIN    = Xyz.X_MIN - 32
    __POSITION_X_MAX    = Xyz.X_MAX + 32
    __POSITION_Y_O      = 0

    # 矩形
    __RECTS = [
        [ -8,  -4,   7,   3, ], 
        [-20, -21,  19,   9, ], 
    ]

    # イメージ
    __IMAGE_U   = 0
    __IMAGE_V   = 136
    __IMAGE_W   = 40
    __IMAGE_H   = 32
    __IMAGE_X   = -20
    __IMAGE_Y   = -21

    # コンストラクタ
    def __init__(self, manager, level):

        # マネージャの取得
        self.__manager = manager

        # 描画の取得
        self.__draw = Draw.get_instance()

        # レベルの初期化
        self.__level = level

        # ライフの初期化
        self.__life = min(16 + 4 * level, 32)

        # ダメージの初期化
        self.__damage = 0

        # 位置の初期化
        self.__position_x = 0
        self.__position_y = -128
        self.__position_z = (Xyz.Z_FAR + Xyz.Z_NEAR) / 2
        
        # 移動の初期化
        self.__move_count = 0
        self.__move_speed = random.randint(0, 1) * 2 - 1

        # 発射の初期化
        self.__fire = 0
        self.__fire_interval = max(45 - 3 * level, 15)

        # 画面位置の初期化
        self.__screen_x = 0
        self.__screen_y = 0
        self.__screen_scale = 0

        # 点滅の初期化
        self.__blink = 0

        # コリジョンの初期化
        self.__collisions = [Collision(), Collision(), ]

        # スコアの初期化
        self.__score = 0

        # 処理の初期化
        self.__process = self.enter
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # ライフの更新
        if self.__process is not None:
            if self.__life > 0 and self.__damage > 0:
                self.__life = max(self.__life - self.__damage, 0)
                self.__damage = 0
                if self.__life == 0:
                    self.set_process(self.bomb)

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

        # スタンパロンの描画
        if (self.__blink & 0x02) == 0:
            pyxel.blt(
                self.__screen_x + EnemyStamperon.__IMAGE_X + Xyz.O_X, 
                self.__screen_y + EnemyStamperon.__IMAGE_Y + Xyz.O_Y, 
                0, 
                EnemyStamperon.__IMAGE_U + self.__screen_scale * EnemyStamperon.__IMAGE_W, 
                EnemyStamperon.__IMAGE_V, 
                EnemyStamperon.__IMAGE_W, 
                EnemyStamperon.__IMAGE_H, 
                pyxel.COLOR_BLACK
            )

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # スタンパロンを破棄する
    def delete(self):

        # 示談の破棄
        self.__manager.delete(self)
        self.__process = None

    # スタンパロンが登場する
    def enter(self):

        # 初期化
        if self.__state == 0:

            # ミュージックの再生
            pyxel.playm(Const.MUSIC_BOSS, loop = True)

            # 初期化の完了
            self.__state = self.__state + 1

        # 移動
        self.__position_y = min(self.__position_y + 1, EnemyStamperon.__POSITION_Y_O)

        # 移動の完了
        if self.__position_y == EnemyStamperon.__POSITION_Y_O:
            self.set_process(self.move)

    # スタンパロンが移動する
    def move(self):

        # 初期化
        if self.__state == 0:

            # 発射の設定
            self.__fire = random.randint(self.__fire_interval, self.__fire_interval + 29)

            # 初期化の完了
            self.__state = self.__state + 1

        # 移動
        self.__position_x = self.__position_x + self.__move_speed
        if self.__position_x <= EnemyStamperon.__POSITION_X_MIN or self.__position_x >= EnemyStamperon.__POSITION_X_MAX:
            self.__move_speed = -self.__move_speed
        self.__move_count = self.__move_count + 1
        self.__position_y = EnemyStamperon.__POSITION_Y_O + 32 * math.sin((self.__move_count << 2) * 2 * math.pi / 256)

        # 発射
        self.__fire = self.__fire - 1
        if self.__fire == 0:
            self.__manager.append(Bullet(self.__manager, self.__position_x, self.__position_y, self.__position_z + 1))
            self.__state = 0

    # スタンパロンが爆発する
    def bomb(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1

        # 点滅の更新
        self.__blink = self.__blink + 1

        # 爆発の生成
        if (self.__blink & 0x04) == 0:
            self.__manager.append(Bomb(self.__manager, self.__position_x + random.randint(-40, 39), self.__position_y + random.randint(-48, 23), self.__position_z, 8))

        # 点滅の完了
        if self.__blink >= 180:
            self.__score = min(50 + 10 * self.__level, 100)
            self.delete()

            # ミュージックの停止
            pyxel.stop(0)
            pyxel.stop(1)
            pyxel.stop(2)

    # 座標情報を計算する
    def calc(self):

        # 画面位置の設定
        screen = Xyz.calc(self.__position_x, self.__position_y, self.__position_z)
        self.__screen_x = screen[0]
        self.__screen_y = screen[1]

        # コリジョンの設定
        self.__collisions[0].set(
            left   = self.__screen_x + EnemyStamperon.__RECTS[0][0], 
            top    = self.__screen_y + EnemyStamperon.__RECTS[0][1], 
            right  = self.__screen_x + EnemyStamperon.__RECTS[0][2], 
            bottom = self.__screen_y + EnemyStamperon.__RECTS[0][3], 
            z      = self.__position_z
        )
        self.__collisions[1].set(
            left   = self.__screen_x + EnemyStamperon.__RECTS[1][0], 
            top    = self.__screen_y + EnemyStamperon.__RECTS[1][1], 
            right  = self.__screen_x + EnemyStamperon.__RECTS[1][2], 
            bottom = self.__screen_y + EnemyStamperon.__RECTS[1][3], 
            z      = self.__position_z
        )

    # ヒット判定を行う
    def hit(self, target):

        # ヒットの判定
        result = Enemy.HIT_NONE
        if self.__process is not None and self.__life > self.__damage:
            if self.__collisions[0].hit(target):
                result = Enemy.HIT_DAMAGE
            elif self.__collisions[1].hit(target):
                result = Enemy.HIT_NOEFFECT
        return result

    # ダメージを食らう
    def damage(self):

        # ダメージの更新
        self.__damage = self.__damage + 1

    # レポートする
    def report(self):

        # スコアを返す
        return self.__score

