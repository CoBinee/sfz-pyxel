# xyz.py - 座標系
#


# 参照
#


# 座標系クラス
#
class Xyz:

    # 座標の領域
    X_MIN   = -64
    X_MAX   =  63
    Y_MIN   = -40
    Y_MAX   =  23
    Z_NEAR  =   0
    Z_FAR   = -47

    # 中心
    O_X     = 64
    O_Y     = 48

    # 距離
    __DISTANCE_YS = [
        0x1f, 0x1e, 0x1d, 0x1c, 0x1b, 0x1a, 0x19, 0x18, 
        0x17, 0x16, 0x15, 0x15, 0x14, 0x13, 0x12, 0x12, 
        0x11, 0x11, 0x10, 0x10, 0x0f, 0x0f, 0x0e, 0x0e, 
        0x0d, 0x0d, 0x0c, 0x0c, 0x0c, 0x0b, 0x0b, 0x0b, 
        0x0a, 0x0a, 0x0a, 0x0a, 0x09, 0x09, 0x09, 0x09, 
        0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 
    ]
    __DISTANCE_SCALES = [
        0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 
        0x02, 0x02, 0x02, 0x02, 0x01, 0x01, 0x01, 0x01, 
        0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    ]

    # 描画座標への変換を行う
    @classmethod
    def calc(cls, x, y, z):

        # Z に応じた XY 位置と大きさを計算
        z = int(min(max(-z, Xyz.Z_NEAR), -Xyz.Z_FAR))
        dy = Xyz.__DISTANCE_YS[z]
        ds = Xyz.__DISTANCE_SCALES[z]
        return [int(x * dy) >> 5, int(y * dy) >> 5, ds, int(dy) << 1]
