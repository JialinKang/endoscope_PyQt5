import numpy as np
import cv2
import matplotlib.pyplot as plt


def convolution(image, kernel, average=False, verbose=False):
    if len(image.shape) == 3:
        print("Found 3 Channels : {}".format(image.shape))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Converted to Gray Channel. Size : {}".format(image.shape))
    else:
        print("Image Shape : {}".format(image.shape))

    print("Kernel Shape : {}".format(kernel.shape))

    if verbose:
        plt.imshow(image, cmap='gray')
        plt.title("Image")
        plt.show()

    image_row, image_col = image.shape
    kernel_row, kernel_col = kernel.shape

    output = np.zeros(image.shape)

    pad_height = int((kernel_row - 1) / 2)
    pad_width = int((kernel_col - 1) / 2)

    padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))

    padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image

    if verbose:
        plt.imshow(padded_image, cmap='gray')
        plt.title("Padded Image")
        plt.show()

    for row in range(image_row):
        for col in range(image_col):
            output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])
            if average:
                output[row, col] /= kernel.shape[0] * kernel.shape[1]

    print("Output Image size : {}".format(output.shape))

    if verbose:
        plt.imshow(output, cmap='gray')
        plt.title("Output Image using {}X{} Kernel".format(kernel_row, kernel_col))
        plt.show()

    return output

def sobel_edge_detection(image, filter, verbose=False):
    new_image_x = convolution(image, filter, verbose)

    if verbose:
        plt.imshow(new_image_x, cmap='gray')
        plt.title("Horizontal Edge")
        plt.show()

    new_image_y = convolution(image, np.flip(filter.T, axis=0), verbose)

    if verbose:
        plt.imshow(new_image_y, cmap='gray')
        plt.title("Vertical Edge")
        plt.show()

    gradient_magnitude = np.sqrt(np.square(new_image_x) + np.square(new_image_y))

    gradient_magnitude *= 255.0 / gradient_magnitude.max()

    if verbose:
        plt.imshow(gradient_magnitude, cmap='gray')
        plt.title("Gradient Magnitude")
        plt.show()

    return gradient_magnitude


image = cv2.imread("./images/2.bmp")
cv2.imshow("Original",image)
cv2.waitKey(0)

#R、G、B分量的提取
(B,G,R) = cv2.split(image)#提取R、G、B分量
cv2.imshow("Red",R)
cv2.imshow("Green",G)
cv2.imshow("Blue",B)
cv2.waitKey(0)

filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

img_sobel = sobel_edge_detection(image, filter, verbose=False)
R_sobel = sobel_edge_detection(R, filter, verbose=False)
G_sobel = sobel_edge_detection(G, filter, verbose=False)
B_sobel = sobel_edge_detection(B, filter, verbose=False)



merged = cv2.merge([R_sobel, G_sobel, B_sobel])
# img_hsv = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
# merged_rgb = cv2.cvtColor(merged, cv2.COLOR_BGR2RGB)
# 将 像素值 低于 值域区间[0, 255] 的 像素点 置0

enhance = merged * 0.1 + image * 0.9

enhance *= (enhance>0)
# 将 像素值 高于 值域区间[0, 255] 的 像素点 置255
enhance = enhance * (enhance<=255) + 255 * (enhance>255)
# 将 dtype 转为图片的 dtype : uint8
enhance = enhance.astype(np.uint8)
cv2.imshow("merged",enhance)
cv2.waitKey(0)

enhance_hsv = cv2.cvtColor(enhance,cv2.COLOR_BGR2HSV)

hsvChannels = cv2.split(enhance_hsv)
H = hsvChannels[0]
S = hsvChannels[1]
V = hsvChannels[2]

H_mean = np.mean(H)
H_std = np.std(H)
h_v = H_mean + H_std * 1.1
V_mean = np.mean(V)
V_std = np.std(V)
t_v = V_mean + V_std * 0.9
S_mean = np.mean(S)
S_std = np.std(S)
t_s = S_mean - S_std * 0.1
width, heigh = H.shape

lower = np.array([0, 0, t_v])
upper = np.array([360,t_s,255])
 
mask = cv2.inRange(enhance_hsv, lower, upper)

mask_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

#######################
image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

image_hsvChannels = cv2.split(image_hsv)
H_im = image_hsvChannels[0]
S_im = image_hsvChannels[1]
V_im = image_hsvChannels[2]

H_mean_im = np.mean(H_im)
H_std_im = np.std(H_im)
h_v_im = H_mean_im + H_std_im * 1.1
V_mean_im = np.mean(V_im)
V_std_im = np.std(V_im)
t_v_im = V_mean_im + V_std_im * 0.9
S_mean_im = np.mean(S_im)
S_std_im = np.std(S_im)
t_s_im = S_mean_im - S_std_im * 0.1
width, heigh = H.shape

lower_im = np.array([0, 0, t_v_im])
upper_im = np.array([360,t_s_im,255])
 
mask_im = cv2.inRange(image_hsv, lower_im, upper_im)

mask_rgb_im = cv2.cvtColor(mask_im, cv2.COLOR_BGR2RGB)

cv2.imshow("mask_im",mask_im)
cv2.imshow("mask_rgb",mask_rgb)
cv2.waitKey(0)