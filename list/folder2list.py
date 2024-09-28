# 分类数据集 类别按文件夹组织
# 合并打乱后 划分训练\验证\测试集
# 并以train_list.txt val_list.txt组织

import os
import shutil
from random import shuffle
from utils.progress import Progress


def generator(
    input_dir, output_dir, class_codes, train_proportion=0.8, val_proportion=0.2
):
    all_images = []
    dataset_dir = os.path.join(output_dir, "dataset")

    # 删除原dataset文件夹
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)

    # 遍历根文件夹下的所有分类文件夹
    for class_folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, class_folder)
        # 遍历该分类文件夹下所有文件
        for image_filename in os.listdir(folder_path):
            img_path = os.path.join(folder_path, image_filename)
            # 以元组格式保存 (图片路径,图片分类)
            all_images.append((img_path, class_folder))

    # 打乱图片列表
    shuffle(all_images)

    os.mkdir(dataset_dir)
    os.mkdir(os.path.join(dataset_dir, "train"))
    os.mkdir(os.path.join(dataset_dir, "val"))
    os.mkdir(os.path.join(dataset_dir, "test"))

    train_file = open(os.path.join(dataset_dir, "train_list.txt"), "a")
    val_file = open(os.path.join(dataset_dir, "val_list.txt"), "a")
    test_file = open(os.path.join(dataset_dir, "test_list.txt"), "a")

    train_set_num = round(len(all_images) * train_proportion)
    val_set_num = round(len(all_images) * val_proportion)

    for i in Progress(range(len(all_images))):
        if i < train_set_num:
            copy_type = "train"
            file = train_file
        elif train_set_num <= i <= train_set_num + val_set_num:
            copy_type = "val"
            file = val_file
        else:
            copy_type = "test"
            file = test_file
        shutil.copy(all_images[i][0], os.path.join(dataset_dir, copy_type))
        file.write(
            copy_type
            + "/"
            + os.path.split(all_images[i][0])[1]
            + " "
            + class_codes[all_images[i][1]]
            + "\n"
        )

    train_file.close()
    val_file.close()
    test_file.close()

    print(f"train set {train_set_num}")
    print(f"val   set {val_set_num}")
    print(f"test  set {len(all_images) - (train_set_num + val_set_num)}")


if __name__ == "__main__":
    # 分类名称到编号的映射
    class_dict = {
        "584": "0",
        "491": "1",
        "400": "2",
        "472": "3",
        "127": "4",
        "393": "5",
    }
    # 原始数据集根路径(纯英文)
    dir1 = "C:\\Users\\LIN_L\\Downloads\\Garbage classification"
    # 新数据集保存路径(纯英文)
    dir2 = "C:\\Users\\LIN_L\\Downloads"
    # 设置训练\验证集比例
    # 若二值相加为1,则不划分验证集,反之,比例为1-train_p-val_p
    train_p = 0.8
    val_p = 0.2

    generator(
        input_dir=dir1,
        output_dir=dir2,
        class_codes=class_dict,
        train_proportion=train_p,
        val_proportion=val_p,
    )
