import os
from random import shuffle
from utils.log import log
from utils.progress import Progress


class BaseLoader:
    def __init__(self):
        # 文件路径
        self.__path = ""
        # 数据是否被划分
        self.__spilt_status = False
        # 划分数据保存位置
        self.__spilt = {
            "train": [],
            "val": [],
            "test": []
        }
        # 原始数据保存位置
        self.__data = {}

    def list_file_clean(self, files):
        # 清空根目录下xxx_list.txt文件
        for file in files:
            if file in ["train_list.txt", "val_list.txt", "test_list.txt"]:
                os.remove(f"{self.__path}/{file}")

    # 读取数据
    def load(self, path: str):
        self.__path = path
        scan_loop = -1
        folder_names = []
        for path, sub_dir, files in os.walk(path):
            # 单文件夹扫描
            if scan_loop == -1 and len(sub_dir) == 0:
                folder_name = os.path.basename(path)
                # 更新数据
                self.__data[folder_name] = files
                # 更新文件夹名
                folder_names.append(folder_name)
                msg = f"folder-name={folder_name} num={len(files)}"
                log("Loader", msg, level=0)
                break

            # 多文件夹扫描
            # 第一轮
            if scan_loop == -1 and len(sub_dir) > 0:
                folder_names = sub_dir
                scan_loop += 1
                self.list_file_clean(files)
            # 第二轮起
            else:
                folder_name = folder_names[scan_loop]
                self.__data[folder_name] = files

                msg = f"folder-name={folder_name} num={len(files)}"
                log("Loader", msg, level=0)

                scan_loop += 1

        log("Loader", "file load complete", level=1)

    # 获取数据
    def get(self):
        if self.__spilt_status:
            return self.__data
        else:
            return self.__spilt

    # 数据选取
    def cut(self, prop=0.8):
        if 0 <= prop <= 1:
            for k, v in self.__data.items():
                v = v[:round(len(v) * prop)]
                self.__data[k] = v
                log("Loader", f"Number of {k} remaining - {len(v)}", level=0)

            log("Loader", "file cut complete", level=1)
        else:
            log("Loader", f"Invalid value {prop}", level=2)

    # 数据乱序
    def shuffle(self):
        for k in self.__data.keys():
            shuffle(self.__data[k])
        log("Loader", "file shuffle complete", level=1)

    # 数据划分
    def split(self, train_prop, val_prop):
        if train_prop + val_prop > 1:
            log("Loader", f"Invalid value {train_prop} {val_prop}", level=2)
            log("Loader", "loader will use default prop [0.8 0.2]", level=2)
            train_prop = 0.8
            val_prop = 0.2

        for k in self.__data.keys():
            v = self.__data[k]
            train_index = len(v) * train_prop
            val_index = len(v) * val_prop + train_index

            for index in Progress(range(len(v)), model="Loader", title=f"folder {k} split"):
                if index < train_index:
                    self.__spilt["train"].append(f"{k}/{v[index]}")
                elif train_index <= index <= val_index:
                    self.__spilt["val"].append(f"{k}/{v[index]}")
                else:
                    self.__spilt["test"].append(f"{k}/{v[index]}")
        log("Loader", "file split complete", level=1)
