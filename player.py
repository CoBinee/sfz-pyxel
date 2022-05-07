# player.py - プレイヤ
#


# 参照
#
import pyxel
from system.draw import Draw
from system.input import Input
from actor import Actor
from manager import Manager
from collision import Collision
from xyz import Xyz
from shot import Shot
from bomb import Bomb


# プレイヤクラス
#
class Player(Actor):

    # ライフ
    LIFE_MAXIMUM  = 8

    # 位置
    __POSITION_X_MIN    = Xyz.X_MIN + 8
    __POSITION_X_MAX    = Xyz.X_MAX - 7
    __POSITION_Y_MIN    = Xyz.Y_MIN + 8
    __POSITION_Y_MAX    = Xyz.Y_MAX - 7

    # 速度
    __SPEED_X = 1
    __SPEED_Y = 1
    __SPEED_Z = 0

    # 矩形
    __RECTS = [
        -2, -2,  1,  1, 
    ]

    # 点滅
    __BLINK_DAMAGE  = 45

    # イメージ
    __IMAGE_U   = 0
    __IMAGE_V   = 48
    __IMAGE_W   = 24
    __IMAGE_H   = 16
    __IMAGE_X   = -12
    __IMAGE_Y   = -8

    # コンストラクタ
    def __init__(self, manager):

        # マネージャの取得
        self.__manager = manager

        # 描画の取得
        self.__draw = Draw.get_instance()

        # 入力の取得
        self.__input = Input.get_instance()

        # ライフの初期化
        self.__life = Player.LIFE_MAXIMUM

        # ダメージの初期化
        self.__damage = 0

        # 位置の初期化
        self.__position_x = 0
        self.__position_y = 0
        self.__position_z = Xyz.Z_NEAR

        # 画面位置の初期化
        self.__screen_x = 0
        self.__screen_y = 0

        # コリジョンの初期化
        self.__collision = Collision()

        # アニメーションの初期化
        self.__animation = 0

        # 点滅の初期化
        self.__blink = 0

        # 処理の初期化
        self.__process = self.play
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # ライフの更新
        if self.__process is not None:
            if self.__damage > 0:
                self.__life = max(self.__life - self.__damage, 0)
                self.__damage = 0
                if self.__life > 0:
                    self.__blink = Player.__BLINK_DAMAGE
                else:
                    self.__manager.append(Bomb(self.__manager, self.__position_x, self.__position_y, self.__position_z, 32))
                    self.set_process(None)

        # 点滅の更新
        self.__blink = max(self.__blink - 1, 0)

        # 処理の実行
        if self.__process is not None:
            self.__process()

        # 座標情報の計算
        if self.__process is not None:
            self.calc()

        # 描画の追加
        if self.__process is not None:
            self.__draw.append(0, self.draw)

    # フレーム毎の描画を行う
    def draw(self):
        
        # オパオパの描画
        if self.__life > 0:
            if (self.__blink & 0x02) == 0x00:
                pyxel.blt(
                    self.__screen_x + Player.__IMAGE_X + Xyz.O_X, 
                    self.__screen_y + Player.__IMAGE_Y + Xyz.O_Y, 
                    0, 
                    Player.__IMAGE_U + ((self.__animation >> 3) & 0x01) * Player.__IMAGE_W, 
                    Player.__IMAGE_V, 
                    Player.__IMAGE_W, 
                    Player.__IMAGE_H, 
                    pyxel.COLOR_BLACK
                )

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # プレイヤを破棄する
    def delete(self):

        # 示談の破棄
        self.__manager.delete(self)
        self.__process = None

    # プレイヤが待機する
    def idle(self):
        pass

    # プレイヤを操作する
    def play(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1

        # 移動
        if self.__input.is_push(Input.KEY_UP):
            self.__position_y = max(self.__position_y - Player.__SPEED_Y, Player.__POSITION_Y_MIN)
        elif self.__input.is_push(Input.KEY_DOWN):
            self.__position_y = min(self.__position_y + Player.__SPEED_Y, Player.__POSITION_Y_MAX)
        if self.__input.is_push(Input.KEY_LEFT):
            self.__position_x = max(self.__position_x - Player.__SPEED_X, Player.__POSITION_X_MIN)
        elif self.__input.is_push(Input.KEY_RIGHT):
            self.__position_x = min(self.__position_x + Player.__SPEED_X, Player.__POSITION_X_MAX)

        # 発射
        if self.__blink == 0 and self.__input.is_edge(Input.KEY_FIRE):
            self.__manager.append(Shot(self.__manager, self.__position_x, self.__position_y, self.__position_z - 1))

        # アニメーションの更新
        self.__animation = self.__animation + 1

    # 座標情報を計算する
    def calc(self):

        # 画面位置の設定
        self.__screen_x = self.__position_x
        self.__screen_y = self.__position_y

        # コリジョンの設定
        self.__collision.set(
            left   = self.__screen_x + Player.__RECTS[0], 
            top    = self.__screen_y + Player.__RECTS[1], 
            right  = self.__screen_x + Player.__RECTS[2], 
            bottom = self.__screen_y + Player.__RECTS[3], 
            z      = self.__position_z
        )

    # 生存しているかどうかを判定する
    def is_live(self):

        # 生存の確認
        return self.__process is not None and self.__life > self.__damage

    # コリジョンを取得する
    def get_collision(self):

        # コリジョンの取得
        return self.__collision if self.is_live() and self.__blink == 0 else None

    # ダメージを食らう
    def damage(self):

        # ダメージの更新
        if self.__blink == 0:
            self.__damage = self.__damage + 1

    # ライフを取得する
    def get_life(self):

        # ライフの取得
        return self.__life

    # 位置を取得する
    def get_position(self):

        # 位置の取得
        return [self.__position_x, self.__position_y, self.__position_z] if self.is_live() else None

    # レポートを返す
    def report(self):

        # レポートなし
        return 0
    