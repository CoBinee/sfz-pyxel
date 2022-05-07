# draw.py - 描画ライブラリ
#


# 参照
#
import pyxel
from system.singleton import Singleton

# 描画ライブラリクラス
#
class Draw(Singleton):

    # コンストラクタ
    def __init__(self):

        # コマンドの初期化
        self.__commands = {}

    # 描画をクリアする
    def clear(self):

        # コマンドのクリア
        self.__commands.clear()

    # 描画を追加する
    def append(self, priority, command):

        # コマンドの登録
        if priority in self.__commands:
            self.__commands[priority].append(command)
        else:
            self.__commands.setdefault(priority, [command])

    # 描画を実行する
    def flush(self):

        # コマンドの実行
        if self.__commands:
            for commands in sorted(self.__commands.items()):
                for command in commands[1]:
                    command()

