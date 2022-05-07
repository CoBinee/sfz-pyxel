# title.py - タイトル
#


# 参照
#
import pyxel
import math
import random
from system.input import Input
from const import Const
from scene import Scene
from data import Data


# タイトルクラス
#
class Title(Scene):

    # コンストラクタ
    def __init__(self):

        # 入力の取得
        self.__input = Input.get_instance()

        # データの取得
        self.__data = Data.get_instance()

        # 背景の初期化
        self.__back = random.randint(0, 1)

        # ロゴの初期化
        self.__logo = 0

        # 点滅の初期化
        self.__blink = 0

        # フレームの初期化
        self.__frame = 0

        # 処理の初期化
        self.__process = self.idle
        self.__state = 0

        # 結果の初期化
        self.__result = None

    # フレーム毎の更新を行う
    def update(self):

        # 処理の実行
        if self.__process is not None:
            self.__process()

        # 終了
        return self.__result

    # フレーム毎の描画を行う
    def draw(self):

        # 画面のクリア
        # pyxel.cls(pyxel.COLOR_BLACK)

        # 背景の描画
        u = 128 + 64 * self.__back
        pyxel.blt( 0, 0, 0, u, 96, 64, 72, pyxel.COLOR_BLACK)
        pyxel.blt(64, 0, 0, u, 96, 64, 72, pyxel.COLOR_BLACK)

        # ギャルの描画
        pyxel.blt(64, 0, 0, 192, 168, 64, 72, pyxel.COLOR_BLACK)

        # スコアの描画
        # pyxel.blt(0, 0, 0, 128, 200, 48, 8, pyxel.COLOR_BLACK)
        pyxel.text(6, 2, "TOP {0:5}".format(self.__data.get_score()), pyxel.COLOR_DARKBLUE)

        # ロゴの描画
        pyxel.blt(16, 12 + 4 * math.sin((self.__logo & 0xff) * 2 * math.pi / 256), 0, 128, 168, 48, 40, pyxel.COLOR_BLACK)

        # HIT SPACE BAR の描画
        if (self.__blink & 0x20) == 0:
            s = "HIT SPACE BAR"
            x = 12
            y = 57
            pyxel.text(x - 1, y + 0, s, pyxel.COLOR_DARKBLUE)
            pyxel.text(x + 1, y + 0, s, pyxel.COLOR_DARKBLUE)
            pyxel.text(x + 0, y - 1, s, pyxel.COLOR_DARKBLUE)
            pyxel.text(x + 0, y + 1, s, pyxel.COLOR_DARKBLUE)
            pyxel.text(x + 0, y + 0, s, pyxel.COLOR_WHITE)

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # 待機する
    def idle(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1

        # ロゴの更新
        self.__logo = self.__logo + 1

        # 点滅の更新
        self.__blink = self.__blink + 1

        # FIRE キーの入力
        if self.__input.is_edge(Input.KEY_FIRE):

            # 処理の更新
            self.set_process(self.start)

    # ゲームを開始する
    def start(self):

        # 初期化
        if self.__state == 0:

            # フレームの設定
            self.__frame = 120

            # サウンドの再生
            pyxel.play(3, Const.SOUND_BOOT)

            # 初期化の完了
            self.__state = self.__state + 1

        # ロゴの更新
        self.__logo = self.__logo + 1

        # 点滅の更新
        self.__blink = self.__blink + 8

        # フレームの更新
        self.__frame = self.__frame - 1
        if self.__frame == 0:

            # シーンの遷移
            self.__result = Const.SCENE_GAME
