# actor.py - アクタクラス
#


# 参照
#
from abc import ABC, abstractmethod


# アクタクラス
#
class Actor(ABC):

    # フレーム毎の更新を行う
    @abstractmethod
    def update(self):
        pass

    # レポートする
    @abstractmethod
    def report(self):
        pass

