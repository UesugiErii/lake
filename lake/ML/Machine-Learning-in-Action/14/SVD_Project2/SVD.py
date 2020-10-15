import numpy as np
from numpy import linalg as la


# 加载并转换数据
def imgLoadData(filename):
    myl = []
    # 打开文本文件，并从文件以数组方式读入字符
    for line in open(filename).readlines():
        newRow = []
        for i in range(32):
            newRow.append(int(line[i]))
        myl.append(newRow)
    myMat = np.mat(myl)
    return myMat


"""
函数说明：分析Sigma的长度取值

Parameters:
    Sigma - Sigma值
    loopNum - 循环次数
    
Returns:
    总方差的集合（总能量值）

Modify:
    2018-08-09
"""


def analyse_data(Sigma, loopNum=20):
    # 总方差的集合（总能量值）
    Sig2 = Sigma ** 2
    SigmaSum = np.sum(Sig2)
    for i in range(loopNum):
        # 根据自己的业务情况，进行处理，设置对应的Sigma次数
        # 通常保留矩阵80%~90%的能量，就可以得到重要的特征并去除噪声
        SigmaI = np.sum(Sig2[:i + 1])
        print('主成分：%s, 方差占比: %s%%' % (format(i + 1, '2.0f'), format(SigmaI / SigmaSum * 100, '4.2f')))


# 打印矩阵
def printMat(inMat, thresh=0.8):
    # 由于矩阵保护了浮点数，因此定义浅色和深色，遍历所有矩阵元素，大于阈值打印1，否则打印0
    for i in range(32):
        for k in range(32):
            if float(inMat[i, k]) > thresh:
                print(1, end='')
            else:
                print(0, end='')
        print()


"""
函数说明：实现图像压缩，允许基于任意给定的奇异值数目来重构图像

Parameters:
    numSV - Sigma长度
    thresh - 判断的阈值
    
Returns:
    None

Modify:
    2018-08-09
"""


def imgCompress(numSV=3, thresh=0.8):
    myMat = imgLoadData('0_5.txt')
    print('****original matrix****')
    printMat(myMat, thresh)
    # 对原始图像进行SVD分解并重构图像
    U, Sigma, VT = la.svd(myMat)
    # 分析插入的Sigma长度
    analyse_data(Sigma, 20)
    SigRecon = np.mat(np.eye(numSV) * Sigma[: numSV])
    reconMat = U[:, :numSV] * SigRecon * VT[:numSV, :]
    print('****reconstructed matrix using %d singular values ****' % numSV)
    printMat(reconMat, thresh)


if __name__ == '__main__':
    imgCompress(2)
