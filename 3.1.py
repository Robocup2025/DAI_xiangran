# -*- coding: utf-8 -*-
"""
OpenCV作业：高斯滤波实现（自动生成测试图版）
无需外部图片！代码自动生成测试图，复制即可运行
功能包含：
1. 手动生成二维高斯滤波核 & 对比OpenCV生成的核
2. 手动实现高斯滤波卷积（含零填充）
3. 手动实现复制边界/镜像边界两种Padding方式
4. 可视化所有结果，方便对比调试
"""

# ====================== 导入必要库 ======================
import numpy as np  # 数值计算核心库
import cv2  # OpenCV库（用于对比核生成）
import matplotlib.pyplot as plt  # 结果可视化

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # 通用无衬线字体，避免中文乱码
plt.rcParams['axes.unicode_minus'] = False


# ====================== 任务1：手动生成高斯核 ======================
def generate_gaussian_kernel(kernel_size, sigma):
    """
    手动实现二维高斯滤波核生成
    :param kernel_size: 核尺寸（必须是奇数，如3/5/7）
    :param sigma: 高斯函数标准差（越大越模糊）
    :return: 归一化后的二维高斯核
    """
    if kernel_size % 2 == 0:
        raise ValueError("核尺寸必须为奇数！请修改为3/5/7等")

    k = kernel_size // 2  # 核半宽
    x, y = np.mgrid[-k:k + 1, -k:k + 1]  # 生成二维坐标网格

    # 二维高斯函数计算
    gaussian = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2)) / (2 * np.pi * sigma ** 2)
    # 归一化（保证核总和为1）
    gaussian /= np.sum(gaussian)

    return gaussian


# ====================== 任务2：OpenCV生成高斯核（用于对比） ======================
def opencv_gaussian_kernel(kernel_size, sigma):
    """调用OpenCV接口生成高斯核，用于和手动实现对比"""
    kernel_1d = cv2.getGaussianKernel(kernel_size, sigma)
    kernel_2d = np.dot(kernel_1d, kernel_1d.T)  # 一维核外积得到二维核
    return kernel_2d


# ====================== 任务3：手动实现两种边界Padding ======================
def padding_replicate(img, pad):
    """手动实现「复制边界」Padding"""
    h, w = img.shape
    padded_img = np.zeros((h + 2 * pad, w + 2 * pad), dtype=img.dtype)

    # 填充原图到中间
    padded_img[pad:pad + h, pad:pad + w] = img
    # 填充上下边界
    padded_img[:pad, pad:pad + w] = img[0:1, :]
    padded_img[pad + h:, pad:pad + w] = img[-1:, :]
    # 填充左右边界
    padded_img[:, :pad] = padded_img[:, pad:pad + 1]
    padded_img[:, pad + w:] = padded_img[:, pad + w - 1:pad + w]

    return padded_img


def padding_reflect(img, pad):
    """手动实现「镜像边界」Padding"""
    h, w = img.shape
    padded_img = np.zeros((h + 2 * pad, w + 2 * pad), dtype=img.dtype)

    # 填充原图到中间
    padded_img[pad:pad + h, pad:pad + w] = img
    # 填充左右镜像
    for i in range(pad):
        padded_img[pad:pad + h, pad - i - 1] = img[:, i]
        padded_img[pad:pad + h, pad + w + i] = img[:, w - i - 1]
    # 填充上下镜像
    for i in range(pad):
        padded_img[pad - i - 1, :] = padded_img[pad + i, :]
        padded_img[pad + h + i, :] = padded_img[pad + h - i - 1, :]

    return padded_img


# ====================== 任务4：手动实现高斯滤波卷积 ======================
def gaussian_filter_manual(img, kernel, pad_mode='zero'):
    """手动实现高斯滤波（卷积操作）"""
    kernel_size = kernel.shape[0]
    pad = kernel_size // 2
    h, w = img.shape

    # 选择Padding模式
    if pad_mode == 'zero':
        padded_img = np.pad(img, pad_width=pad, mode='constant', constant_values=0)
    elif pad_mode == 'replicate':
        padded_img = padding_replicate(img, pad)
    elif pad_mode == 'reflect':
        padded_img = padding_reflect(img, pad)
    else:
        raise ValueError("pad_mode仅支持：zero/replicate/reflect")

    # 初始化滤波结果
    filtered_img = np.zeros_like(img, dtype=np.float32)

    # 逐像素卷积
    for i in range(h):
        for j in range(w):
            window = padded_img[i:i + kernel_size, j:j + kernel_size]
            filtered_img[i, j] = np.sum(window * kernel)

    # 归一化到0-255
    filtered_img = np.clip(filtered_img, 0, 255).astype(np.uint8)

    return filtered_img


# ====================== 主函数：自动生成测试图 + 运行 ======================
if __name__ == "__main__":
    # -------------------- 步骤1：自动生成测试灰度图（无需外部图片） --------------------
    # 生成500x500的全黑灰度图（0=黑，255=白）
    img_arr = np.zeros((500, 500), dtype=np.float32)
    # 在中间画一个150x150的白色方块（方便看滤波效果）
    img_arr[175:325, 175:325] = 255
    print(f"自动生成测试图成功！尺寸：{img_arr.shape}")

    # -------------------- 步骤2：配置参数 --------------------
    kernel_params = [
        (3, 1),  # 3x3核，σ=1
        (5, 2),  # 5x5核，σ=2
        (7, 3)  # 7x7核，σ=3
    ]
    pad_mode = 'zero'  # 可选：zero/replicate/reflect
    pad_width = 20  # Padding对比的填充宽度

    # -------------------- 步骤3：生成高斯核 & 对比 --------------------
    print("\n===== 高斯核对比（手动 vs OpenCV） =====")
    for size, sigma in kernel_params:
        manual_kernel = generate_gaussian_kernel(size, sigma)
        opencv_kernel = opencv_gaussian_kernel(size, sigma)
        # 打印核信息（保留4位小数）
        print(f"\n{size}x{size} σ={sigma} 手动核：")
        print(np.round(manual_kernel, 4))
        print(f"{size}x{size} σ={sigma} OpenCV核：")
        print(np.round(opencv_kernel, 4))
        # 计算核差异
        diff = np.sum(np.abs(manual_kernel - opencv_kernel))
        print(f"核差异总和：{diff:.6f}（越小越一致）")

    # -------------------- 步骤4：手动高斯滤波 & 可视化 --------------------
    filtered_results = []
    for size, sigma in kernel_params:
        kernel = generate_gaussian_kernel(size, sigma)
        filtered_img = gaussian_filter_manual(img_arr, kernel, pad_mode=pad_mode)
        filtered_results.append((filtered_img, f"{size}x{size} σ={sigma}"))

    # 绘制滤波结果对比图
    plt.figure(figsize=(15, 5))
    # 原图
    plt.subplot(1, len(filtered_results) + 1, 1)
    plt.imshow(img_arr, cmap='gray', vmin=0, vmax=255)
    plt.title("Original Image (Test)")
    plt.axis('off')
    # 滤波结果
    for i, (res_img, title) in enumerate(filtered_results):
        plt.subplot(1, len(filtered_results) + 1, i + 2)
        plt.imshow(res_img, cmap='gray', vmin=0, vmax=255)
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.savefig("高斯滤波结果.png", dpi=150, bbox_inches='tight')
    plt.show()

    # -------------------- 步骤5：Padding效果对比 --------------------
    pad_rep = padding_replicate(img_arr, pad_width)
    pad_ref = padding_reflect(img_arr, pad_width)

    # 绘制Padding对比图
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(img_arr, cmap='gray', vmin=0, vmax=255)
    plt.title("Original Image")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(pad_rep, cmap='gray', vmin=0, vmax=255)
    plt.title(f"Replicate Padding (pad={pad_width})")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(pad_ref, cmap='gray', vmin=0, vmax=255)
    plt.title(f"Reflect Padding (pad={pad_width})")
    plt.axis('off')

    plt.tight_layout()
    plt.savefig("Padding对比.png", dpi=150, bbox_inches='tight')
    plt.show()

    print("\n===== 运行完成！结果图已保存到当前目录 =====")