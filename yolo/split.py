import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import random


def copy_files(src_dir, dst_dir, file_names, ext):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    def copy_single_file(name):
        src_file = os.path.join(src_dir, f"{name}{ext}")
        dst_file = os.path.join(dst_dir, f"{name}{ext}")
        shutil.copy(src_file, dst_file)

    # 使用tqdm显示进度条
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(
            tqdm(
                executor.map(copy_single_file, file_names),
                total=len(file_names),
                desc=f"Copying to {dst_dir}",
            )
        )


def split_dataset(
    images_dir, labels_dir=None, output_base_dir="./datasets", ratios=(6, 3, 1)
):
    image_files = [
        f for f in os.listdir(images_dir) if f.endswith(".jpg")
    ]
    random.shuffle(image_files)  # 随机打乱文件列表

    # 计算每个集合的文件数量
    total_files = len(image_files)
    train_files = int(ratios[0] * total_files / sum(ratios))
    val_files = int(ratios[1] * total_files / sum(ratios))
    test_files = total_files - train_files - val_files

    train_names, val_names, test_names = (
        image_files[:train_files],
        image_files[train_files : train_files + val_files],
        image_files[train_files + val_files :],
    )

    # 定义输出目录
    output_dirs = {
        "train": os.path.join(output_base_dir, "train"),
        "val": os.path.join(output_base_dir, "val"),
        "test": os.path.join(output_base_dir, "test"),
    }

    # 确保输出目录存在
    for dir_name in output_dirs.values():
        os.makedirs(dir_name, exist_ok=True)

    # 复制图片和标签
    for split_type, names in [
        ("train", train_names),
        ("val", val_names),
        ("test", test_names),
    ]:
        images_dst = os.path.join(output_dirs[split_type], "images")
        labels_dst = (
            os.path.join(output_dirs[split_type], "labels") if labels_dir else None
        )

        # 复制图片
        copy_files(images_dir, images_dst, names, "")

        # 如果指定了标签目录，则复制标签
        if labels_dir:
            label_names = [
                name.replace(".jpg", ".txt")
                for name in names
                if os.path.exists(
                    os.path.join(labels_dir, name.replace(".jpg", ".txt"))
                )
            ]
            if label_names:
                copy_files(labels_dir, labels_dst, label_names, "")


root_path = "C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019_YOLO\\ccpd_base"
output_dir = "C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019_YOLO\\ccpd_base\\datasets"

split_dataset(root_path + "\\images", root_path + "\\labels", output_dir)
