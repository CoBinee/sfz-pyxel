# data.py - データ
#


# 参照
#
from system.singleton import Singleton


# データクラス
#
class Data(Singleton):

    # コンストラクタ
    def __init__(self):
        
        # スコアの初期化
        self.__score = 100
    
    # スコアの取得
    def get_score(self):

        # スコアの取得
        return self.__score

    # スコアの設定
    def set_score(self, score):

        # スコアの設定
        if self.__score < score:
            self.__score = score
