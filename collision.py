# collision.py - コリジョン
#


# 参照
#


# コリジョンクラス
#
class Collision:

    # ヒット
    __HIT_DEPTH     = 4

    # コンストラクタ
    def __init__(self, left = 0, top = 0, right = 0, bottom = 0, z = 0):

        # パラメータの初期化
        self.__left = left
        self.__top = top
        self.__right = right
        self.__bottom = bottom
        self.__z = z

    # パラメータを設定する
    def set(self, **kwargs):

        # パラメータの設定
        for key, value in kwargs.items():
            if key == "left":
                self.__left = value
            elif key == "top":
                self.__top = value
            elif key == "right":
                self.__right = value
            elif key == "bottom":
                self.__bottom = value
            elif key == "z":
                self.__z = value

    # ヒット判定を行う
    def hit(self, target):

        # 位置との判定
        ## print("({0},{1},{2},{3})/{4} -> ({5},{6},{7},{8})/{9}".format(self.__left, self.__top, self.__right, self.__bottom, self.__z, target.__left, target.__top, target.__right, target.__bottom, target.__z))
        return (self.__z <= target.__z and target.__z < self.__z + Collision.__HIT_DEPTH) and (not (self.__right < target.__left or self.__left > target.__right or self.__bottom < target.__top or self.__top > target.__bottom))


