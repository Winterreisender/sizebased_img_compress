#%%
import cv2
import os
import numpy as np
from functools import lru_cache
from logging import debug as print

# 统一交换方式:
# 文件大小 int (按Byte计)
# 图片: W x H x 4 的 numpy.ndarray
# (图片文件)字节序列: bytes
#%%
def loss_compress(img :np.ndarray, quality :int) -> bytes:
    assert 5 <= quality <= 100
    assert isinstance(quality, int)
    return cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality] )[1].tobytes()

# 算法
# 无损压缩
# 有损压缩: 经验公式预估初始值 -> 指数调整 -> 线性调整
def smart_compress(img, target_size :int) -> bytes: # 请保证target_size<origin_size

    if len(loss_compress(img, 5)) > target_size:
        raise UserWarning('对不起做不到!')

    @lru_cache(16)
    def custom_loss_compress(quality) -> bytes:
        return loss_compress(img, quality)

    def custom_binary_search(target, left, right):
        middle = (left + right) // 2

        middle_result = loss_compress(img, middle)
        middle_size = len(middle_result)

        print(f"l={left}, r={right}, m={middle}, m_size={middle_size}")

        assert left <= right

        if(right - left <= 1): # 左右区间差必须在 2 以上, 否则会无限递归
            return (left, loss_compress(img, left))
        elif(middle_size >= target):
            return custom_binary_search(target, left, middle-1) 
        elif(middle_size < target):
            return custom_binary_search(target, middle, right)# 保证left一定OK,不能加一



    result = custom_binary_search(target_size, 5,99)
    return result
    # raise UserWarning("Minium Quality Reached")
