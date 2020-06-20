# Use Python3 and cv2 change image size

import cv2

crop_size = (400, 560)  # result size  (width,high)

img = cv2.imread('image path')  # read image

img_new = cv2.resize(img, crop_size, interpolation=cv2.INTER_CUBIC)

# CV_INTER_NN - 最近邻插值
# CV_INTER_LINEAR - 双线性插值
# CV_INTER_AREA - 使用象素关系重采样
# CV_INTER_CUBIC - 立方插值

cv2.imwrite("save image path.png", img_new)  # also can save as *.jpg
