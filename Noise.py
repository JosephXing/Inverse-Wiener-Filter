import matplotlib.pyplot as graph
import numpy as np
from numpy import fft
import math
import cv2

# 仿真运动模糊
def motion_process(image_size, motion_angle):
    PSF = np.zeros(image_size)
    print(image_size)
    center_position = (image_size[0] - 1) / 2
    print(center_position)
 
    slope_tan = math.tan(motion_angle * math.pi / 180)
    slope_cot = 1 / slope_tan
    if slope_tan <= 1:
        for i in range(15):
            offset = round(i * slope_tan)  # ((center_position-i)*slope_tan)
            PSF[int(center_position + offset), int(center_position - offset)] = 1
        return PSF / PSF.sum()  # 对点扩散函数进行归一化亮度
    else:
        for i in range(15):
            offset = round(i * slope_cot)
            PSF[int(center_position - offset), int(center_position + offset)] = 1
        return PSF / PSF.sum()


# 对图片进行运动模糊
def make_blurred(input, PSF, eps):
    input_fft = fft.fft2(input)  # 进行二维数组的傅里叶变换
    PSF_fft = fft.fft2(PSF) + eps
    blurred = fft.ifft2(input_fft * PSF_fft)
    blurred = np.abs(fft.fftshift(blurred))
    return blurred


image = cv2.imread('lena512.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
img_h = image.shape[0]
img_w = image.shape[1]
graph.figure(1)
graph.xlabel("Original Image")
graph.gray()
graph.imshow(image)  # 显示原图像

graph.figure(2)
graph.gray()
# 进行运动模糊处理
PSF = motion_process((img_h, img_w), 60)
blurred = np.abs(make_blurred(image, PSF, 1e-3))

blurred_noisy = blurred + 0.01 * blurred.std() * \
                np.random.standard_normal(blurred.shape)  # 添加噪声,standard_normal产生随机的函数

graph.subplot(131)
graph.title("Original Image")
graph.gray()
graph.imshow(image)  # 显示添加噪声且运动模糊的图像

graph.subplot(132)
graph.title("motion blurred")
graph.gray()
graph.imshow(blurred)  # 显示添加噪声且运动模糊的图像

graph.subplot(133)
graph.title("motion & noisy blurred & sigma=0.01")
graph.gray()
graph.imshow(blurred_noisy)  # 显示添加噪声且运动模糊的图像

graph.show()