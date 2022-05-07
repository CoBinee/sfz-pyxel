# singleton.py - シングルトン
#


# 参照
#


# シングルトンクラス
#
class Singleton:

    # インスタンス
    __instance = None

    # インスタンスを生成する
    def __new__(cls):

        # new の抑制
        raise NotImplementedError("can not initialize via constructor.")

    # インスタンスを生成する
    @classmethod
    def __internal_new__(cls):

        # インスタンスの生成
        instance = super().__new__(cls)

        # インスタンスの初期化
        if instance is not None:
            instance.__init__()

        # 終了
        return instance

    # インスタンスを取得する
    @classmethod
    def get_instance(cls):

        # インスタンスの生成
        if cls.__instance is None:
            cls.__instance = cls.__internal_new__()

        # インスタンスを返す
        return cls.__instance
