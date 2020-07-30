import numpy as np
from PIL import Image


# 加载灰度图并转换数据
def imgLoadData(filename):
    gray = Image.open('1.jpg').convert('L')
    return np.array(gray)


def analyse_data(Sigma, loopNum=20):
    # 总方差的集合（总能量值）
    Sig2 = Sigma ** 2
    SigmaSum = np.sum(Sig2)
    for i in range(loopNum):
        # 根据自己的业务情况，进行处理，设置对应的Sigma次数
        # 通常保留矩阵80%~90%的能量，就可以得到重要的特征并去除噪声
        SigmaI = np.sum(Sig2[:i + 1])
        print('主成分：%s, 方差占比: %s%%' % (format(i + 1, '2.0f'), format(SigmaI / SigmaSum * 100, '4.2f')))


def imgCompress():
    data = imgLoadData('./1.jpg')
    im = Image.fromarray(data)
    im.show()
    # 对原始图像进行SVD分解并重构图像
    U, Sigma, VT = np.linalg.svd(data)
    # 分析插入的Sigma长度
    analyse_data(Sigma, 20)
    for numSV in [32, 16, 8, 4, 2, 1]:
        SigRecon = np.eye(numSV) * Sigma[: numSV]
        reconMat = np.dot(np.dot(U[:, :numSV], SigRecon), VT[:numSV, :])
        # You need to close the previous image window before calling show() each time,
        # It is recommended to use debugging run, normal run cannot be displayed
        im = Image.fromarray(reconMat)
        im.show()


if __name__ == '__main__':
    imgCompress()
