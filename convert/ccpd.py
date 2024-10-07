import os
import re
import shutil
import cv2

from concurrent.futures.thread import ThreadPoolExecutor

from utils.log import log
from utils.progress import Progress
from utils.fileloader.BaseLoader import BaseLoader


class CCPD:
    def __init__(self):
        # system level
        self.__upload_type = {
            0: self.to_yolo,
            1: self.to_ocr
        }
        self.__rename_index = 0
        self.__threadpool = None
        self.__spilt_type = False

        # base
        self._images = None
        self._input_path = None
        self._output_path = None

        # extra
        self._copy_image = False
        self._rename = False

    def image_load(self,
                   input_path,
                   output_path=None,
                   train_prop=0.8,
                   val_prop=0.2,
                   cut_prop=0.01,
                   max_workers=10,
                   copy=False,
                   rename=False,  # 当copy被置为ture时 此项有效
                   spilt=False,
                   shuffle=False, ):
        self._input_path = input_path
        self._output_path = output_path
        self.mkdir()

        loader = BaseLoader()
        loader.load(input_path)

        if shuffle:
            loader.shuffle()
        if cut_prop != 0:
            loader.cut(cut_prop)
        if spilt:
            loader.split(train_prop=train_prop, val_prop=val_prop)
            self.__spilt_type = True

        self._images = loader.get()
        self._copy_image = copy
        self._rename = rename
        self.__threadpool = ThreadPoolExecutor(max_workers=max_workers)

        log("CCPD", "file load complete", level=1)

    def mkdir(self):
        if self._output_path is None:
            root = os.path.join(self._input_path, f"../{os.path.basename(self._input_path)}_yolo")
            self._output_path = root
        else:
            root = self._output_path
        if os.path.exists(root):
            shutil.rmtree(root)
        os.mkdir(root)
        os.mkdir(os.path.join(root, "images"))
        os.mkdir(os.path.join(root, "labels"))
        os.mkdir(os.path.join(root, "ocr"))

        log("CCPD", "folder build complete", level=1)

    def to_yolo(self, image: str):
        image_path = os.path.join(self._input_path, image)

        img = cv2.imread(image_path)
        height, width = img.shape[0], img.shape[1]

        str1 = re.findall("-\d+&\d+_\d+&\d+-", image)[0][1:-1]
        str2 = re.split("[&_]", str1)

        x0, y0, x1, y1 = map(int, str2)
        x = round((x0 + x1) / 2 / width, 6)
        y = round((y0 + y1) / 2 / height, 6)
        w = round((x1 - x0) / width, 6)
        h = round((y1 - y0) / height, 6)

        image_name = os.path.splitext(image)[0]
        out_path = os.path.join(self._output_path, "labels")

        if self._copy_image:
            image_copy_path = os.path.join(self._output_path, "images")

            if self._rename:
                image_name = str(self.__rename_index)
                self.__rename_index += 1
            shutil.copy(image_path, image_copy_path + "/" + image_name + ".jpg")

        txt_file = os.path.join(out_path, image_name + ".txt")

        with open(txt_file, "w") as f:
            f.write(" ".join(["0", str(x), str(y), str(w), str(h)]))

    # TODO ccpd ocr数据提取
    def to_ocr(self):
        pass

    # TODO 多数据类型自适应功能
    def thread_upload(self, type_code):
        futures = []
        for i in [key for key in self._images.keys()]:
            for image in Progress(self._images[i],
                                  module="CCPD",
                                  title="file uploading",
                                  level=0):
                future = self.__threadpool.submit(self.__upload_type[type_code], image)
                futures.append(future)

        for future in Progress(futures,
                               module="CCPD",
                               title="data converting",
                               level=0):
            future.result()

        log(module="CCPD", msg="data converting complete", level=1)


if __name__ == "__main__":
    data_path = "D:/Datasets/CCPD2019/ccpd_base"

    ccpd = CCPD()
    ccpd.image_load(input_path=data_path,
                    train_prop=0.8,
                    val_prop=0.2,
                    cut_prop=0.001,
                    copy=False,
                    rename=True,
                    spilt=False,
                    shuffle=False)
    ccpd.thread_upload(type_code=0)
    print()
