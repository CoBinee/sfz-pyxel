# input.py - 入力ライブラリ
#


# 参照
#
import pyxel
from system.singleton import Singleton

# 入力ライブラリクラス
#
class Input(Singleton):

    # キー
    KEY_UP      = 0
    KEY_DOWN    = 1
    KEY_LEFT    = 2
    KEY_RIGHT   = 3
    KEY_FIRE    = 4

    # コンストラクタ
    def __init__(self):
        pass

    # キーが押されているかどうかを判定する
    def is_push(self, key):

        # キーの入力
        result = False
        if key == Input.KEY_UP:
            result = pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD_1_UP)
        elif key == Input.KEY_DOWN:
            result = pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD_1_DOWN)
        elif key == Input.KEY_LEFT:
            result = pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD_1_LEFT)
        elif key == Input.KEY_RIGHT:
            result = pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT)
        elif key == Input.KEY_FIRE:
            result = pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_ENTER) or pyxel.btn(pyxel.GAMEPAD_1_A)
        
        # 終了
        return result

    # キーが押され始めたかどうかを判定する
    def is_edge(self, key):

        # キーの入力
        result = False
        if key == Input.KEY_UP:
            result = pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.GAMEPAD_1_UP)
        elif key == Input.KEY_DOWN:
            result = pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD_1_DOWN)
        elif key == Input.KEY_LEFT:
            result = pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD_1_LEFT)
        elif key == Input.KEY_RIGHT:
            result = pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.GAMEPAD_1_RIGHT)
        elif key == Input.KEY_FIRE:
            result = pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_ENTER) or pyxel.btnp(pyxel.GAMEPAD_1_A)
        
        # 終了
        return result



