from source.AdaptiveHaffmanCoding import AdaptiveHaffman
from compressors import BWT_MTF_AHA
from compressors import BWT_MTF_RLE_AHA
from compressors import LZ77_AHA
from compressors import BWT_MTF_HA
from compressors import BWT_MTF_RLE_HA
from compressors import LZ77_HA


if __name__ == "__main__":
    # AdaptiveHaffman.test_compress()
    # BWT_MTF_AHA.test_compress()
    # BWT_MTF_RLE_AHA.test_compress()
    # LZ77_AHA.test_compress()
    # BWT_MTF_HA.test_compress(1)
    # BWT_MTF_HA.test_compress(2)
    # BWT_MTF_HA.test_compress(3)
    BWT_MTF_RLE_HA.test_compress(1)
    BWT_MTF_RLE_HA.test_compress(2)
    BWT_MTF_RLE_HA.test_compress(3)
    # LZ77_HA.test_compress(1)
    # LZ77_HA.test_compress(2)
    LZ77_HA.test_compress(3)


    # Adaptive  Haffman Compress: 63862234
    # BWT_MTF_AHA: 29689596
    # BWT_MTF_RLE_AHA: 28383203
    # LZ77_AHA: 51805938
    # BWT_MTF_HA
    # 1: 29691186
    # BWT_MTF_HA
    # 2: 27376282
    # BWT_MTF_HA
    # 3: 28238620
    # LZ77_HA 1:  51801815
    # 48984048