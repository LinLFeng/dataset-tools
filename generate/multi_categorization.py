import os
from utils.fileloader.MultiLoader import MultiLoader
from utils.progress import Progress
from utils.log import log


def multi_categorization(
        path,
        train_prop=0.8,
        val_prop=0.2,
        cut_prop=0.01,
        folder_code=None,
        shuffle=False,
):
    log("multi_categorization", "build start", level=1)

    folders_loader = MultiLoader()
    folders_loader.load(path, folder_code=folder_code)
    if shuffle:
        folders_loader.shuffle()
    if cut_prop != 0:
        folders_loader.cut(cut_prop)
    folders_loader.split(train_prop=train_prop, val_prop=val_prop)
    image = folders_loader.get()

    for file_name in ["train", "val", "test"]:
        with open(os.path.join(path, f"{file_name}_list.txt"), "a") as file:
            for j in Progress(image[file_name],
                              model="multi_categorization",
                              title=f"{file_name}_list.txt building"):
                file.write(f"{j}\n")

    log("multi_categorization", "build complete", level=1)


if __name__ == "__main__":
    # 分类名称到编号的映射
    class_dict = {
        "cardboard": "584",
        "glass": "491",
        "metal": "400",
        "paper": "472",
        "plastic": "127",
        "trash": "393",
    }
    # 原始数据集根路径(纯英文)
    dir1 = "D:\\Datasets\\Garbage classification"
    # 设置训练\验证集比例
    # 若二值相加为1,则不划分验证集,反之,比例为1-train_p-val_p
    train_p = 0.8
    val_p = 0.2
    # 数据选择比例
    cut_p = 1
    # 数据乱序
    shu = True

    multi_categorization(
        path=dir1,
        train_prop=train_p,
        val_prop=val_p,
        cut_prop=cut_p,
        folder_code=class_dict,
        shuffle=shu,
    )
