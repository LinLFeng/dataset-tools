import os
from PIL import Image, ImageDraw
import numpy as np
from tqdm import tqdm
import shutil


def create_mask(label_path, image_size, mask_path):
    try:
        with open(label_path, "r") as f:
            labels = f.read().strip().split()
            if len(labels) < 5:  # 确保有足够的标签数据
                print(f"Error: Not enough labels in {label_path}")
                return
            x_min, y_min, width, height = map(float, labels[1:])

            t_width = width * image_size[0]
            t_height = height * image_size[1]

            x_c = x_min * image_size[0]
            y_c = y_min * image_size[1]

            x0 = x_c - t_width / 2
            y0 = y_c - t_height / 2
            x1 = x_c + t_width / 2
            y1 = y_c + t_height / 2

            # 确保边界框在图片范围内
            if x0 < 0 or y0 < 0 or x1 > image_size[0] or y1 > image_size[1]:
                print(f"Error: Bounding box out of image bounds in {label_path}")
                return

            # 创建掩码并绘制矩形
            mask_img = Image.new("L", image_size, 0)
            draw = ImageDraw.Draw(mask_img)
            draw.rectangle([x0, y0, x1, y1], fill=255)
            mask_img.save(mask_path)
    except Exception as e:
        print(f"Error processing {label_path}: {e}")


def process_images(root_dir, output_dir):
    # 创建输出目录
    os.makedirs(os.path.join(output_dir, "mask"), exist_ok=True)

    # 读取images目录下的所有图片
    image_files = [
        f
        for f in os.listdir(os.path.join(root_dir, "images"))
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    # 遍历图片和标签
    for image_file in tqdm(image_files, desc="Processing images"):
        # 构造图片和标签的完整路径
        image_path = os.path.join(root_dir, "images", image_file)
        # 假设标签文件名与图片文件名相同且扩展名为.txt
        label_path = os.path.join(
            root_dir, "labels", image_file.rsplit(".", 1)[0] + ".txt"
        )

        # 检查标签文件是否存在
        if not os.path.exists(label_path):
            print(f"Label file {label_path} does not exist.")
            continue

        # 读取图片大小
        with Image.open(image_path) as img:
            image_size = img.size

        # 生成掩码图片并保存
        output_mask_path = os.path.join(
            output_dir, "mask", image_file.rsplit(".", 1)[0] + ".png"
        )
        create_mask(label_path, image_size, output_mask_path)


# 设置根目录和输出目录
root_dir = (
    "C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019_YOLO\\ccpd_base\\datasets\\val"
)
output_dir = (
    "C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019_YOLO\\ccpd_base\\datasets\\val"
)

# 调用函数处理图片
process_images(root_dir, output_dir)
