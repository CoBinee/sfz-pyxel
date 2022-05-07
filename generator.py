# generator.py - ジェネレータ
#


# 参照
#
import pyxel
import random
from actor import Actor
from manager import Manager
from xyz import Xyz
from enemy import Enemy
from enemy_pole import EnemyPole
from enemy_dorarinfuras import EnemyDorarinfuras
from enemy_jurii import EnemyJurii
from enemy_onyanma import EnemyOnyanma
from enemy_stamperon import EnemyStamperon


# ジェネレータクラス
#
class Generator(Actor):

    # コンストラクタ
    def __init__(self, manager):

        # マネージャの取得
        self.__manager = manager

        # レベルの初期化
        self.__level = 0

        # フレームの初期化
        self.__frame = 0

        # カウントの初期化
        self.__count = 0

        # インデックスの初期化
        self.__index = 0

        # パラメータの初期化
        self.__params = [0, 0, ]

        # ザコの初期化
        self.__zakos = [self.pole, self.dorarinfuras, self.dorarinfuras, self.jurii, self.jurii, self.onyanma, self.onyanma, self.onyanma]
        self.__zako = None

        # 処理の初期化
        self.__process = self.zako
        self.__state = 0

    # フレーム毎の更新を行う
    def update(self):

        # 処理の実行
        if self.__process is not None:
            self.__process()

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # ザコを生成する
    def zako(self):

        # 初期化
        if self.__state == 0:

            # ザコをまぜる
            # length = len(self.__zakos)
            # for i in range(length):
            #     j = random.randint(0, length - 1)
            #     t = self.__zakos[i]
            #     self.__zakos[i] = self.__zakos[j]
            #     self.__zakos[j] = t
            self.__zako = None

            # インデックの設定
            self.__index = 0

            # フレームの設定
            self.__frame = 180

            # 初期化の完了
            self.__state = self.__state + 1

        # フレームの更新
        if self.__frame > 0:
            self.__frame = self.__frame - 1
        else:

            # ザコの存在
            if self.__zako is None:

                # ザコの取得
                self.__zako = self.__zakos[random.randint(0, len(self.__zakos) - 1)]

                # カウントの設定
                self.__count = min(random.randint(self.__level + 3, self.__level + 5), 10)

                # パラメータの設定
                self.__params[0] = random.randint(0, 1) * 2 - 1
                self.__params[1] = random.randint(0, 1) * 2 - 1

            # ザコの生成
            self.__frame = self.__zako()
            self.__count = self.__count - 1

            # ザコの生成の完了
            if self.__count == 0:
                self.__index = self.__index + 1

                # ザコの生成の継続
                if self.__index < len(self.__zakos):
                    self.__zako = None
                    self.__frame = max(300 - self.__level * 30, 90)

                # 全てのザコの生成の完了
                else:
                    self.set_process(self.boss)

    # ボスを生成する
    def boss(self):

        # 初期化
        if self.__state == 0:

            # フレームの設定
            self.__frame = 90

            # 初期化の完了
            self.__state = self.__state + 1

        # エネミーがいなくなるのを待つ
        if self.__manager.get_actors(Enemy) is None:

            # フレームの更新
            self.__frame = self.__frame - 1
            if self.__frame == 0:

                # スタンパロンの生成
                self.stamperon()

                # 処理の更新
                self.set_process(self.idle)

    # 待機する
    def idle(self):

        # エネミーがいなくなるのを待つ
        if self.__manager.get_actors(Enemy) is None:

            # レベルを上げる
            self.__level = self.__level + 1

            # 処理の更新
            self.set_process(self.zako)

    # 柱を生成する
    def pole(self):
        self.__manager.append(EnemyPole(self.__manager, self.__level))
        return 30

    # ドラリンフラーを生成する
    def dorarinfuras(self):
        self.__manager.append(EnemyDorarinfuras(self.__manager, self.__level, self.__params[0], self.__params[1]))
        return 15

    # ジェリィを生成する
    def jurii(self):
        self.__manager.append(EnemyJurii(self.__manager, self.__level))
        return 30

    # オニャンマを生成する
    def onyanma(self):
        self.__manager.append(EnemyOnyanma(self.__manager, self.__level))
        return 45

    # スタンパロンを生成する
    def stamperon(self):
        self.__manager.append(EnemyStamperon(self.__manager, self.__level))
        return 0

    # レポートを返す
    def report(self):

        # レポートなし
        return 0
    