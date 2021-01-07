# 这个文件用来将BP-CF论文中的数据整合进去, 然后重新画图

import matplotlib.pyplot as plt

plt_data_x = [10, 20, 30, 40, 50, 60]
plt_data_y_LICM = [0.7777242985245753, 0.7649019271629508, 0.759399977005078, 0.7584570767348644, 0.7574269144956333, 0.7568756938455794]
plt_data_y_cosine = [0.8214342388634586, 0.8086946549647708, 0.8065888937817799, 0.8073106732944716, 0.8075673566820236, 0.8079365110211246]
plt_data_y_3 = [0.8308358509431902, 0.8293916974620071, 0.8353140441658793, 0.8417051565196165, 0.8481927012337407, 0.8543324226983553]
plt_data_y_4 = [0.809, 0.792, 0.786, 0.787, 0.788, 0.789]

plt.plot(plt_data_x, plt_data_y_LICM, c='r',  marker="o", label='LICM-Based CF')
plt.plot(plt_data_x, plt_data_y_cosine, c='b', marker="s", label='Cosine-Based CF')
plt.plot(plt_data_x, plt_data_y_3, c='g', marker="^", label='Adjust Cosine-Based CF')
plt.plot(plt_data_x, plt_data_y_4, c='c', marker="x", label='BP-CF')

plt.legend()

# 指定dpi=300，图片尺寸为 1800*1200
plt.savefig("final.png", dpi=300)
