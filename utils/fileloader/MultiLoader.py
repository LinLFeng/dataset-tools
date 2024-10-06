import os
from utils.log import log
from utils.progress import Progress
from utils.fileloader.BaseLoader import BaseLoader


class MultiLoader(BaseLoader):
    def __init__(self):
        BaseLoader.__init__(self)
        self._folder_code = {}

    # 默认文件夹编号
    def __default_folder_code(self):
        index = 0
        for i in self._data.keys():
            self._folder_code[i] = index
            index += 1
        log("Loader", "default folder code upload", level=1)

    # 自定义文件夹编号
    def __folder_code_upload(self, folder_code):
        data_keys = [key for key in self._data.keys()]
        folder_code_keys = [key for key in folder_code.keys()]
        for i in folder_code_keys:
            if i not in data_keys:
                log("Loader", "class code can not be found", level=2)
                log("Loader", "loader will use default class code", level=2)
                return
        self._folder_code = folder_code
        log("Loader", "folder code upload", level=1)

    def load(self, path: str, folder_code=None):
        BaseLoader.load(self, path)
        if folder_code is not None:
            self.__folder_code_upload(folder_code)
        else:
            self.__default_folder_code()

    def split(self, train_prop, val_prop):
        if train_prop + val_prop > 1:
            log("Loader", f"Invalid value {train_prop} {val_prop}", level=2)
            log("Loader", "loader will use default prop [0.8 0.2]", level=2)
            train_prop = 0.8
            val_prop = 0.2
        for k in Progress([key for key in self._data.keys()],
                          model="Loader",
                          title="data split",
                          level=0):
            v = self._data[k]
            train_index = len(v) * train_prop
            val_index = len(v) * val_prop + train_index
            for image_index in range(len(v)):
                if image_index < train_index:
                    self._spilt["train"].append(
                        f"{k}/{v[image_index]} {self._folder_code[k]}")
                elif train_prop < image_index <= val_index:
                    self._spilt["val"].append(
                        f"{k}/{v[image_index]} {self._folder_code[k]}")
                else:
                    self._spilt["test"].append(
                        f"{k}/{v[image_index]} {self._folder_code[k]}")
        self._spilt_status = True
        log("Loader", "file split complete", level=1)
