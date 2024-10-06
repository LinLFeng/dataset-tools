import os
from random import shuffle
from utils.log import normal_log, warning_log, error_log, process_log
from utils.progress import Progress


class BaseLoader:
    def __init__(self):
        self.__path = ""
        # 数据是否被划分
        self.__spilt_status = False
        self.__data = {
            "spilt": {"train": [],
                      "val": [],
                      "test": []},
            "load": {},
            "load_dirs": [],
            "folder_code": {}
        }

    # 读取数据
    def load(self, path: str, folder_code=None):
        self.__path = path

        file_scan_loop = -1
        files_num = 0
        for path, sub_dir, files in os.walk(self.__path):  # 后续轮次
            if file_scan_loop >= 0:
                self.__data["load"][self.__data["load_dirs"][file_scan_loop]] = files
                files_num += len(files)
                msg = f"folder-name={self.__data['load_dirs'][file_scan_loop]} "
                msg += f"code={self.__data['folder_code'][self.__data['load_dirs'][file_scan_loop]]} "
                msg += f"num={len(files)}"
                normal_log("Loader", msg)
                file_scan_loop += 1

            # 单文件夹扫描
            if file_scan_loop == -1 and len(sub_dir) == 0:
                self.__data["only"] = files
                break
            # 多文件夹扫描
            # 第一轮
            if file_scan_loop == -1 and len(sub_dir) > 0:
                # 清空根目录下xxx_list.txt文件
                for file in files:
                    if file in ["train_list.txt", "val_list.txt", "test_list.txt"]:
                        os.remove(f"{path}/{file}")
                self.__data['load_dirs'] = sub_dir
                file_scan_loop += 1

                # 自定义类型编码
                if folder_code is not None:
                    # 编码映射上传验证
                    self.folder_code_upload(folder_code)
                else:
                    self.default_folder_code()

        normal_log("Loader", f"Total files --- {files_num}")
        process_log("Loader", "file load complete")

    def before_load(self):
        for files in self.__data["load_dirs"]:
            if os.path.isdir(files):
                os.remove(files)

    # 默认文件夹编号
    def default_folder_code(self):
        index = 0
        for i in self.__data["load_dirs"]:
            self.__data["folder_code"][i] = index
            index += 1

    # 自定义文件夹编号
    def folder_code_upload(self, folder_code):
        for i in folder_code.keys():
            if i not in self.__data["load_dirs"]:
                warning_log("Loader", "class code can not be found")
                warning_log("Loader", "loader will use default class code")
                break
            self.__data["folder_code"] = folder_code

    # 获取数据
    def get_data(self):
        if self.__spilt_status:
            return self.__data["load"]
        else:
            return self.__data["spilt"]

    # 获取文件夹编号数据
    def get_code(self):
        return self.__data["folder_code"]

    # 数据选取
    def cut(self, prop=0.8):
        if 0 <= prop <= 1:
            for k in self.__data["load_dirs"]:
                v = self.__data["load"][k]
                cut_index = round(len(v) * prop)
                self.__data["load"][k] = v[:cut_index]
        process_log("Loader", "file cut complete")

    # 数据乱序
    def shuffle(self):
        for k in self.__data["load_dirs"]:
            v = self.__data["load"][k]
            shuffle(v)
        process_log("Loader", "file shuffle complete")

    # TODO: 多分类数据划分功能
    # 数据划分
    def split(self, train_prop, val_prop):
        if train_prop + val_prop > 1:
            train_prop = 0.8
            val_prop = 0.2

        for k in Progress(self.__data["load_dirs"], model="Loader", title="data split"):
            # v 文件夹中图片
            v = self.__data["load"][k]
            train_index = len(v) * train_prop
            val_index = len(v) * val_prop + train_index
            for image_index in range(len(v)):
                if image_index < train_index:
                    self.__data["spilt"]["train"].append(
                        f"{k}/{v[image_index]} {self.__data['folder_code'][k]}")
                elif train_prop < image_index <= val_index:
                    self.__data["spilt"]["val"].append(
                        f"{k}/{v[image_index]} {self.__data['folder_code'][k]}")
                else:
                    self.__data["spilt"]["test"].append(
                        f"{k}/{v[image_index]} {self.__data['folder_code'][k]}")

    # 以下为对原始数据集的修改功能
    # TODO: 基于比例精简数据集功能
    # 基于原始数据集的比例精简
    def prop_streamlining(self):
        pass

    # TODO: 拷贝功能
    # 在别处生成处理后的数据集
    def build_new_folder(self):
        pass


class YoloLoader(BaseLoader):
    """
    yolo数据加载功能
    images 图片文件 | labels 标签文件
    在读取时执行完整性验证
    无法相互匹配到的将被抛弃
    """

    # TODO:load功能待重写
    def load(self, path):
        self.__path = path
        print("-" * 10, "yolo file load start", "-" * 10)
        images_path = os.path.join(path, "images")
        labels_path = os.path.join(path, "labels")

        # 路径校验
        for target_path, name in [(images_path, "images"), (labels_path, "labels")]:
            if not os.path.exists(target_path):
                print(f"Unable to find {name} folder")
                print("-" * 10, "yolo file load error", "-" * 10)
                return -1

        # 数据完整性校验
        files_list = {}
        for file_type in ["images", "labels"]:
            for file in os.listdir(os.path.join(path, file_type)):
                image_files, _ = os.path.split(file)
                files_list[f"{file_type}"].append(image_files)

        # final {"yolo":[yolo_data]}
        self.__data["yolo"] = list(set(files_list["images"]).intersection(set(files_list["labels"])))
        del files_list

        print(f"Total files --- {len(self.__data)}")
        print("-" * 10, "yolo file load complete", "-" * 10)
