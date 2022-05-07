# scene.py - シーンクラス
#


# 参照
#
from abc import ABC, abstractmethod


# シーンクラス
#
class Scene(ABC):

    # フレーム毎の更新を行う
    @abstractmethod
    def update(self):
        pass

    # フレーム毎の描画を行う
    @abstractmethod
    def draw(self):
        pass
    
