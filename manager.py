# manager.py - マネージャ
#


# 参照
#
from actor import Actor


# マネージャクラス
#
class Manager():

    # レポート
    __REPORT_MAXIMUM    = 99999

    # コンストラクタ
    def __init__(self):

        # アクタの初期化
        self.__actors = []

        # 破棄の初期化
        self.__deletes = []

        # レポートの初期化
        self.__report = 0

    # アクタをクリアする
    def clear(self):

        # アクタのクリア
        self.__actors.clear()

    # アクタを追加する
    def append(self, actor):

        # アクタの登録
        self.__actors.append(actor)

    # アクタを削除する
    def remove(self, actor):

        # アクタの削除
        self.__actors.remove(actor)

    # アクタを破棄する
    def delete(self, actor):

        # アクタの削除
        self.__actors.remove(actor)

        # アクタの破棄の予約
        self.__deletes.append(actor)
    
    # アクタを更新する
    def update(self):

        # アクタの更新
        for actor in self.__actors:
            actor.update()

        # アクタの破棄
        for actor in self.__deletes:
            self.__report = min(self.__report + actor.report(), Manager.__REPORT_MAXIMUM)
            del actor
        self.__deletes.clear()

    # 指定したクラスのアクタを取得する
    def get_actors(self, cls):

        # アクタの取得
        a = [i for i in self.__actors if isinstance(i, cls)]
        return a if a  else None

    # レポートを取得する
    def get_report(self):

        # レポートの取得
        return self.__report
