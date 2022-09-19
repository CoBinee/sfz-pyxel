# application.py - アプリケーション
#


# 参照
#
import pyxel
from system.draw import Draw
from system.input import Input
from const import Const
from data import Data
from title import Title
from game import Game

# アプリケーションクラス
#
class Application:

    # コンストラクタ
    def __init__(self):

        # Pyxel の初期化
        pyxel.init(128, 72, title = "SFZ", display_scale = 4, fps = 60)

        # システムの初期化
        self.__draw = Draw.get_instance()
        self.__input = Input.get_instance()

        # データの初期化
        self.__data = Data.get_instance()

        # リソースの読み込み
        filename = "assets/resource.pyxres"
        pyxel.load(filename)
        filename = "assets/bank0.png"
        pyxel.image(0).load(0, 0, filename)

        # シーンの初期化
        self.__scene = None
        self.__trans = Const.SCENE_TITLE

        # Pyxel の実行
        pyxel.run(self.update, self.draw)

    # フレーム毎の更新を行う
    def update(self):

        # シーンの作成
        if self.__trans is not None:
            if self.__scene is not None:
                del self.__scene
                self.__scene = None
            if self.__trans == Const.SCENE_TITLE:
                self.__scene = Title()
            elif self.__trans == Const.SCENE_GAME:
                self.__scene = Game()
            self.__trans = None

        # シーンの更新
        if self.__scene is not None:
            self.__trans = self.__scene.update()
        
    # フレーム毎の描画を行う
    def draw(self):

        # シーンの描画
        if self.__scene is not None:
            self.__scene.draw()


# アプリケーションのエントリポイント
#
Application()

