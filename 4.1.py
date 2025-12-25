# -*- coding: utf-8 -*-
"""
Homework3：梯度算子/Canny/Harris/直方图均衡化（完整实现）
自动生成测试图，无需外部图片，复制即可运行
包含所有任务的可视化结果，自动保存到当前目录
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ====================== 工具函数：卷积操作（复用） ======================
def convolve(img, kernel):
    """手动实现卷积（适用于Sobel/Harris等任务）"""
    kernel_size = kernel.shape[0]
    pad = kernel_size // 2
    # 零填充
    padded_img = np.pad(img, pad_width=pad, mode='constant', constant_values=0)
    h, w = img.shape
    result = np.zeros_like(img, dtype=np.float32)

    # 逐像素卷积
    for i in range(h):
        for j in range(w):
            window = padded_img[i:i + kernel_size, j:j + kernel_size]
            result[i, j] = np.sum(window * kernel)
    return result


# ====================== 任务1：Sobel梯度算子实现 ======================
def sobel_gradient(img_gray):
    """
    实现Sobel梯度算子，返回x/y方向梯度、梯度幅值
    :param img_gray: 灰度图（np数组）
    :return: Gx, Gy, gradient_mag
    """
    # 1. 构造Sobel核
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)

    # 2. 卷积计算x/y方向梯度
    Gx = convolve(img_gray, sobel_x)
    Gy = convolve(img_gray, sobel_y)

    # 3. 计算梯度幅值并归一化到0-255
    gradient_mag = np.sqrt(Gx ** 2 + Gy ** 2)
    gradient_mag = (gradient_mag / gradient_mag.max()) * 255  # 归一化
    gradient_mag = gradient_mag.astype(np.uint8)

    return Gx, Gy, gradient_mag


# ====================== 任务2：手动实现Canny边缘检测 ======================
def canny_edge_detection(img_gray, sigma=1.0, high_thresh=60, low_thresh=30):
    """
    手动实现Canny边缘检测，返回各环节结果
    :param img_gray: 灰度图
    :param sigma: 高斯滤波标准差
    :param high_thresh: 双阈值-高阈值
    :param low_thresh: 双阈值-低阈值
    :return: 高斯滤波图, 梯度幅值图, NMS图, 最终边缘图
    """
    # 步骤1：高斯滤波（平滑降噪）
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), sigmaX=sigma)

    # 步骤2：计算梯度幅值+方向（用Sobel）
    Gx, Gy, gradient_mag = sobel_gradient(img_blur)
    # 计算梯度方向（弧度转角度，0-180°）
    gradient_dir = np.arctan2(Gy, Gx) * (180 / np.pi)
    gradient_dir[gradient_dir < 0] += 180  # 统一到0-180°

    # 步骤3：非极大值抑制（NMS）
    h, w = gradient_mag.shape
    nms_img = np.zeros_like(gradient_mag, dtype=np.uint8)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            dir_angle = gradient_dir[i, j]
            # 确定梯度方向对应的邻域（4个方向）
            if (0 <= dir_angle < 22.5) or (157.5 <= dir_angle <= 180):
                neighbor1 = gradient_mag[i, j + 1]
                neighbor2 = gradient_mag[i, j - 1]
            elif 22.5 <= dir_angle < 67.5:
                neighbor1 = gradient_mag[i + 1, j + 1]
                neighbor2 = gradient_mag[i - 1, j - 1]
            elif 67.5 <= dir_angle < 112.5:
                neighbor1 = gradient_mag[i + 1, j]
                neighbor2 = gradient_mag[i - 1, j]
            else:  # 112.5-157.5
                neighbor1 = gradient_mag[i + 1, j - 1]
                neighbor2 = gradient_mag[i - 1, j + 1]
            # 仅保留局部极大值
            if (gradient_mag[i, j] >= neighbor1) and (gradient_mag[i, j] >= neighbor2):
                nms_img[i, j] = gradient_mag[i, j]

    # 步骤4：双阈值边缘连接
    edge_img = np.zeros_like(nms_img, dtype=np.uint8)
    # 强边缘（>高阈值）直接保留
    strong_edges = (nms_img >= high_thresh)
    edge_img[strong_edges] = 255
    # 弱边缘（低阈值< <高阈值）：与强边缘连通则保留
    weak_edges = (nms_img >= low_thresh) & (nms_img < high_thresh)
    # 8邻域连通性判断
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if weak_edges[i, j]:
                if np.any(strong_edges[i - 1:i + 2, j - 1:j + 2]):
                    edge_img[i, j] = 255

    return img_blur, gradient_mag, nms_img, edge_img


# ====================== 任务3：手动实现Harris角点检测 ======================
def harris_corner_detection(img_gray, ksize=3, sigma=1.0, alpha=0.04, thresh=0.01, window_size=3):
    """
    手动实现Harris角点检测，返回角点坐标
    :param img_gray: 灰度图
    :param ksize: Sobel核尺寸
    :param sigma: 高斯滤波标准差
    :param alpha: Harris参数（0.04-0.06）
    :param thresh: 响应函数R的阈值（相对最大值的比例）
    :param window_size: NMS窗口大小
    :return: 角点坐标列表
    """
    # 步骤1：小方差高斯滤波
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), sigmaX=0.5)

    # 步骤2：计算Ix、Iy（用Sobel）
    Ix = cv2.Sobel(img_blur, cv2.CV_64F, 1, 0, ksize=ksize)
    Iy = cv2.Sobel(img_blur, cv2.CV_64F, 0, 1, ksize=ksize)

    # 步骤3：计算Ix²、Iy²、IxIy，并高斯滤波
    Ix2 = cv2.GaussianBlur(Ix ** 2, (3, 3), sigmaX=sigma)
    Iy2 = cv2.GaussianBlur(Iy ** 2, (3, 3), sigmaX=sigma)
    IxIy = cv2.GaussianBlur(Ix * Iy, (3, 3), sigmaX=sigma)

    # 步骤4：构造M矩阵，计算R
    det_M = (Ix2 * Iy2) - (IxIy ** 2)
    trace_M = Ix2 + Iy2
    R = det_M - alpha * (trace_M ** 2)

    # 步骤5：阈值筛选（取R的最大值的thresh比例作为阈值）
    R_max = R.max()
    R_thresh = R_max * thresh
    candidates = (R >= R_thresh)

    # 步骤6：非极大值抑制（NMS）
    h, w = R.shape
    corners = []
    pad = window_size // 2
    for i in range(pad, h - pad):
        for j in range(pad, w - pad):
            if candidates[i, j]:
                # 取窗口内的最大值
                window = R[i - pad:i + pad + 1, j - pad:j + pad + 1]
                if R[i, j] == window.max():
                    corners.append((j, i))  # 注意：OpenCV是(x,y)即(col,row)

    return np.array(corners)


# ====================== 任务4：手动实现直方图均衡化 ======================
def histogram_equalization(img_gray):
    """
    手动实现直方图均衡化，返回均衡化图像+直方图数据
    :param img_gray: 灰度图
    :return: 均衡化图像, 原直方图, 均衡化后直方图
    """
    # 步骤1：计算原图像直方图
    hist_original, _ = np.histogram(img_gray.flatten(), bins=256, range=[0, 256])

    # 步骤2：计算累积分布函数（CDF）
    cdf = hist_original.cumsum()
    cdf = cdf / cdf.max()  # 归一化到0-1

    # 步骤3：生成像素映射表（CDF→0-255）
    cdf_mapped = (cdf * 255).astype(np.uint8)

    # 步骤4：替换原图像素
    img_eq = cdf_mapped[img_gray]

    # 步骤5：计算均衡化后的直方图
    hist_equalized, _ = np.histogram(img_eq.flatten(), bins=256, range=[0, 256])

    return img_eq, hist_original, hist_equalized


# ====================== 主函数：运行所有任务+可视化 ======================
if __name__ == "__main__":
    # 自动生成测试图（500x500，含方块+线条，方便检测边缘/角点）
    img = np.zeros((500, 500), dtype=np.uint8)
    # 画方块
    img[100:200, 100:200] = 200
    img[300:400, 300:400] = 150
    # 画十字线
    img[200:300, 250:260] = 255
    img[250:260, 200:300] = 255
    print("自动生成测试图成功！尺寸：", img.shape)

    # -------------------- 任务1：Sobel梯度算子可视化 --------------------
    Gx, Gy, grad_mag = sobel_gradient(img)
    # 可视化
    plt.figure(figsize=(12, 8))
    plt.subplot(221);
    plt.imshow(img, cmap='gray');
    plt.title("Original Image");
    plt.axis('off')
    plt.subplot(222);
    plt.imshow(Gx, cmap='gray');
    plt.title("Sobel-X Gradient");
    plt.axis('off')
    plt.subplot(223);
    plt.imshow(Gy, cmap='gray');
    plt.title("Sobel-Y Gradient");
    plt.axis('off')
    plt.subplot(224);
    plt.imshow(grad_mag, cmap='gray');
    plt.title("Gradient Magnitude");
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("1_Sobel_Result.png", dpi=150)
    plt.show()

    # -------------------- 任务2：Canny边缘检测可视化 --------------------
    img_blur, grad_mag, nms_img, canny_edge = canny_edge_detection(img)
    # 可视化
    plt.figure(figsize=(12, 8))
    plt.subplot(221);
    plt.imshow(img, cmap='gray');
    plt.title("Original");
    plt.axis('off')
    plt.subplot(222);
    plt.imshow(img_blur, cmap='gray');
    plt.title("Gaussian Blur");
    plt.axis('off')
    plt.subplot(223);
    plt.imshow(nms_img, cmap='gray');
    plt.title("NMS Result");
    plt.axis('off')
    plt.subplot(224);
    plt.imshow(canny_edge, cmap='gray');
    plt.title("Canny Edge");
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("2_Canny_Result.png", dpi=150)
    plt.show()

    # -------------------- 任务3：Harris角点检测（不同窗口大小对比） --------------------
    # 测试3种窗口大小
    window_sizes = [3, 5, 7]
    plt.figure(figsize=(15, 5))
    for idx, ws in enumerate(window_sizes):
        corners = harris_corner_detection(img, window_size=ws)
        img_corner = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # 绘制角点
        for (x, y) in corners:
            cv2.circle(img_corner, (x, y), 2, (0, 0, 255), -1)
        # 可视化
        plt.subplot(1, 3, idx + 1)
        plt.imshow(cv2.cvtColor(img_corner, cv2.COLOR_BGR2RGB))
        plt.title(f"Harris Corners (Window={ws})")
        plt.axis('off')
    plt.tight_layout()
    plt.savefig("3_Harris_Result.png", dpi=150)
    plt.show()

    # -------------------- 任务4：直方图均衡化可视化 --------------------
    img_eq, hist_ori, hist_eq = histogram_equalization(img)
    # 可视化图像+直方图
    plt.figure(figsize=(12, 8))
    # 图像对比
    plt.subplot(221);
    plt.imshow(img, cmap='gray');
    plt.title("Original");
    plt.axis('off')
    plt.subplot(222);
    plt.imshow(img_eq, cmap='gray');
    plt.title("Equalized");
    plt.axis('off')
    # 直方图对比
    plt.subplot(223);
    plt.bar(range(256), hist_ori);
    plt.title("Original Histogram")
    plt.subplot(224);
    plt.bar(range(256), hist_eq);
    plt.title("Equalized Histogram")
    plt.tight_layout()
    plt.savefig("4_HistEqual_Result.png", dpi=150)
    plt.show()

    print("所有任务完成！结果图已保存到当前目录")