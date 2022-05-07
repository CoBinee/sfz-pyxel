# enemy.py - エネミー
#


# 参照
#
from abc import abstractmethod
from actor import Actor


# エネミークラス
#
class Enemy(Actor):

    # ヒット
    HIT_NONE        = 0
    HIT_DAMAGE      = 1
    HIT_NOEFFECT    = 2

    # ヒット判定を行う
    @abstractmethod
    def hit(self, target):
        pass

    # ダメージを食らう
    @abstractmethod
    def damage(self):
        pass

