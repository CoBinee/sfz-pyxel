# game.py - ゲーム
#


# 参照
#
import pyxel
from system.draw import Draw
from system.input import Input
from const import Const
from scene import Scene
from data import Data
from manager import Manager
from player import Player
from generator import Generator
from field import Field
from enemy import Enemy
from shot import Shot
from bullet import Bullet


# ゲームクラス
#
class Game(Scene):

    # イメージ
    __IMAGE_LIFE_U      = 64
    __IMAGE_LIFE_V      = 48
    __IMAGE_LIFE_W      = 8
    __IMAGE_LIFE_H      = 8
    __IMAGE_LIFE_X      = 1
    __IMAGE_LIFE_Y      = 0
    __IMAGE_SCORE_U     = 64
    __IMAGE_SCORE_V     = 56
    __IMAGE_SCORE_W     = 56
    __IMAGE_SCORE_H     = 8
    __IMAGE_SCORE_X     = 72
    __IMAGE_SCORE_Y     = 0
    __IMAGE_START_U     = 64
    __IMAGE_START_V     = 136
    __IMAGE_START_W     = 64
    __IMAGE_START_H     = 16
    __IMAGE_START_X     = 32
    __IMAGE_START_Y     = 28
    __IMAGE_OVER_U      = 64
    __IMAGE_OVER_V      = 152
    __IMAGE_OVER_W      = 64
    __IMAGE_OVER_H      = 16
    __IMAGE_OVER_X      = 32
    __IMAGE_OVER_Y      = 28

    # コンストラクタ
    def __init__(self):

        # 描画の取得
        self.__draw = Draw.get_instance()

        # 入力の取得
        self.__input = Input.get_instance()

        # データの取得
        self.__data = Data.get_instance()

        # マネージャの初期化
        self.__manager = Manager()

        # プレイヤの初期化
        self.__player = Player(self.__manager)

        # ジェネレータの初期化
        self.__generator = Generator(self.__manager)

        # フィールドの初期化
        self.__field = Field(self.__manager)

        # フレームの初期化
        self.__frame = 0

        # 処理の初期化
        self.__process = self.start
        self.__state = 0

        # 結果の初期化
        self.__result = None

    # フレーム毎の更新を行う
    def update(self):

        # 描画のクリア
        self.__draw.clear()

        # 処理の実行
        if self.__process is not None:
            self.__process()

        # 終了
        return self.__result

    # フレーム毎の描画を行う
    def draw(self):

        # 画面のクリア
        # pyxel.cls(pyxel.COLOR_BLACK)

        # 描画の実行
        self.__draw.flush()

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # ゲームを開始する
    def start(self):

        # 初期化
        if self.__state == 0:

            # アクタの登録
            self.__manager.append(self.__player)
            self.__manager.append(self.__field)

            # ミュージックの再生
            pyxel.playm(Const.MUSIC_START, loop = False)

            # 初期化の完了
            self.__state = self.__state + 1

        # マネージャの更新
        self.__manager.update()

        # ステータスの描画
        self.__draw.append(10000, self.draw_status)

        # スタートの描画
        self.__draw.append(10000, self.draw_start)

        # ミュージックの監視
        if not pyxel.play_pos(0):

            # 処理の更新
            self.set_process(self.play)

    # ゲームをプレイする
    def play(self):

        # 初期化
        if self.__state == 0:

            # アクタの登録
            self.__manager.append(self.__generator)

            # 初期化の完了
            self.__state = self.__state + 1

        # ヒット判定
        self.hit()

        # マネージャの更新
        self.__manager.update()

        # ステータスの描画
        self.__draw.append(10000, self.draw_status)

        # プレイヤの死亡
        if not self.__player.is_live():

            # 処理の更新
            self.set_process(self.over)

        # ミュージックの再生
        if not pyxel.play_pos(0):
            pyxel.playm(Const.MUSIC_GAME, loop = True)

    # ゲームオーバーになる
    def over(self):

        # 初期化
        if self.__state == 0:

            # アクタの削除
            self.__manager.remove(self.__generator)

            # フレームの設定
            self.__frame = 90

            # ミュージックの停止
            pyxel.stop(0)
            pyxel.stop(1)
            pyxel.stop(2)

            # 初期化の完了
            self.__state = self.__state + 1

        # マネージャの更新
        self.__manager.update()

        # ステータスの描画
        self.__draw.append(10000, self.draw_status)

        # フレームの更新
        if self.__frame > 0:
            self.__frame = self.__frame - 1
            if self.__frame == 0:

                # ミュージックの再生
                pyxel.playm(Const.MUSIC_OVER, loop = False)

        # フレームの更新の完了
        else:

            # ゲームオーバーの描画
            self.__draw.append(10000, self.draw_over)

            # FIRE キーの押下
            if self.__input.is_edge(Input.KEY_FIRE):

                # 処理の更新
                self.set_process(self.end)

    # ゲームを閉じる
    def end(self):

        # 初期化
        if self.__state == 0:

            # スコアの更新
            self.__data.set_score(self.__manager.get_report())

            # フレームの設定
            self.__frame = 30

            # ミュージックの停止
            pyxel.stop(0)
            pyxel.stop(1)
            pyxel.stop(2)

            # サウンドの再生
            pyxel.play(3, Const.SOUND_CLICK)

            # 初期化の完了
            self.__state = self.__state + 1

        # マネージャの更新
        self.__manager.update()

        # ステータスの描画
        self.__draw.append(10000, self.draw_status)

        # ゲームオーバーの描画
        self.__draw.append(10000, self.draw_over)

        # フレームの更新
        self.__frame = self.__frame - 1
        if self.__frame == 0:
        
            # シーンの遷移
            self.__result = Const.SCENE_TITLE

    # ヒット判定を行う
    def hit(self):

        # プレイヤの取得
        pc = self.__player.get_collision()

        # エネミーの取得
        enemys = self.__manager.get_actors(Enemy)

        # 自弾の取得
        shots = self.__manager.get_actors(Shot)

        # 敵弾の取得
        bullets = self.__manager.get_actors(Bullet)

        # 自弾とエネミーの判定
        if shots is not None and enemys is not None:
            for shot in shots:
                sc = shot.get_collision()
                if sc is not None:
                    for enemy in enemys:
                        hit = enemy.hit(sc)
                        if hit == Enemy.HIT_DAMAGE:
                            enemy.damage()
                            shot.damage()
                        elif hit == Enemy.HIT_NOEFFECT:
                            shot.rebound()
        
        # プレイヤの判定
        if pc is not None:

            # プレイヤと敵弾の判定
            if bullets is not None:
                for bullet in bullets:
                    if bullet.hit(pc):
                        bullet.damage()
                        self.__player.damage()

            # プレイヤとエネミーの判定
            if enemys is not None:
                for enemy in enemys:
                    if enemy.hit(pc) != Enemy.HIT_NONE:
                        enemy.damage()
                        self.__player.damage()

    # ステータスを描画する
    def draw_status(self):

        # ライフの描画
        life = self.__player.get_life()
        for i in range(life):
            pyxel.blt(
                i * Game.__IMAGE_LIFE_W + Game.__IMAGE_LIFE_X, 
                Game.__IMAGE_LIFE_Y, 
                0, 
                Game.__IMAGE_LIFE_U + 1 * Game.__IMAGE_LIFE_W, 
                Game.__IMAGE_LIFE_V, 
                Game.__IMAGE_LIFE_W, 
                Game.__IMAGE_LIFE_H, 
                pyxel.COLOR_BLACK
            )
        for i in range(life, Player.LIFE_MAXIMUM):
            pyxel.blt(
                i * Game.__IMAGE_LIFE_W + Game.__IMAGE_LIFE_X, 
                Game.__IMAGE_LIFE_Y, 
                0, 
                Game.__IMAGE_LIFE_U + 0 * Game.__IMAGE_LIFE_W, 
                Game.__IMAGE_LIFE_V, 
                Game.__IMAGE_LIFE_W, 
                Game.__IMAGE_LIFE_H, 
                pyxel.COLOR_BLACK
            )
        pyxel.blt(
            Player.LIFE_MAXIMUM * Game.__IMAGE_LIFE_W + Game.__IMAGE_LIFE_X, 
            Game.__IMAGE_LIFE_Y, 
            0, 
            Game.__IMAGE_LIFE_U + 2 * Game.__IMAGE_LIFE_W, 
            Game.__IMAGE_LIFE_V, 
            Game.__IMAGE_LIFE_W, 
            Game.__IMAGE_LIFE_H, 
            pyxel.COLOR_BLACK
        )

        # スコアの描画
        pyxel.blt(
            Game.__IMAGE_SCORE_X, 
            Game.__IMAGE_SCORE_Y, 
            0, 
            Game.__IMAGE_SCORE_U, 
            Game.__IMAGE_SCORE_V, 
            Game.__IMAGE_SCORE_W, 
            Game.__IMAGE_SCORE_H, 
            pyxel.COLOR_BLACK
        )
        pyxel.text(
            Game.__IMAGE_SCORE_X + 6, 
            Game.__IMAGE_SCORE_Y + 2, 
            "SCORE {0:5d}".format(self.__manager.get_report()), 
            pyxel.COLOR_WHITE
        )

    # スタートを描画する
    def draw_start(self):

        # スタートの描画
        pyxel.blt(
            Game.__IMAGE_START_X, 
            Game.__IMAGE_START_Y, 
            0, 
            Game.__IMAGE_START_U, 
            Game.__IMAGE_START_V, 
            Game.__IMAGE_START_W, 
            Game.__IMAGE_START_H, 
            pyxel.COLOR_BLACK
        )

    # ゲームオーバーを描画する
    def draw_over(self):

        # スタートの描画
        pyxel.blt(
            Game.__IMAGE_OVER_X, 
            Game.__IMAGE_OVER_Y, 
            0, 
            Game.__IMAGE_OVER_U, 
            Game.__IMAGE_OVER_V, 
            Game.__IMAGE_OVER_W, 
            Game.__IMAGE_OVER_H, 
            pyxel.COLOR_BLACK
        )

