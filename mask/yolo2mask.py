# 使用yolo格式的标签来生成掩码文件
# 生成位置 数据集根目录
# 无划分训练/验证集功能


import os
from concurrent.futures.thread import ThreadPoolExecutor
from PIL import Image, ImageDraw
from tqdm import tqdm
import shutil


def draw_mask(image, root_dir):
    image_path = os.path.join(root_dir, "images", image)

    # 标签名与图片名相同
    label_path = os.path.join(
        root_dir, "labels", image.rsplit(".", 1)[0] + ".txt"
    )

    # 检查标签文件是否存在
    if not os.path.exists(label_path):
        print(f"Label file {label_path} does not exist.")
        return

    # 读取图片大小
    with Image.open(image_path) as img:
        image_size = img.size
        img.close()

    with open(label_path, "r") as f:
        labels = f.read().strip().split()
        if len(labels) < 5:
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
        mask_img.save(os.path.join(root_dir, "mask", image.rsplit(".", 1)[0] + ".png"))
        f.close()


def process_images(root_dir):
    mask_dir = os.path.join(root_dir, "mask")

    # 删除原mask文件夹
    if os.path.exists(mask_dir):
        shutil.rmtree(mask_dir)

    # 创建输出目录
    os.makedirs(mask_dir, exist_ok=True)

    # 读取images目录下的所有图片
    image_files = [
        f
        for f in os.listdir(os.path.join(root_dir, "images"))
        if f.lower().endswith(".jpg")
    ]

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for image in image_files:
            future = executor.submit(draw_mask, image, root_dir)
            futures.append(future)

        for future in tqdm(futures, total=len(image_files)):
            future.result()


if __name__ == "__main__":
    # 路径
    dir1 = "C:\\Users\\LIN_L\\Downloads\\ccpd_2k"

    process_images(root_dir=dir1)
