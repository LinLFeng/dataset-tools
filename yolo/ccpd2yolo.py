import os
import os.path
import re
import shutil
import cv2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def find_images(input_dir):
    result = []
    for filedir, subdir, file_name_list in os.walk(input_dir):
        for filename in file_name_list:
            apath = os.path.join(filedir, filename)
            result.append(apath)
    return result


def work_process(filedir: str, filename, output_image_dir, output_label_dir):
    if filedir.endswith(".jpg"):
        img = cv2.imread(filedir)
        height, width = img.shape[0], img.shape[1]

        str1 = re.findall("-\d+&\d+_\d+&\d+-", filedir)[0][1:-1]
        str2 = re.split("[&_]", str1)
        x0, y0, x1, y1 = map(int, str2)

        x = round((x0 + x1) / 2 / width, 6)
        y = round((y0 + y1) / 2 / height, 6)
        w = round((x1 - x0) / width, 6)
        h = round((y1 - y0) / height, 6)

        img_file = os.path.join(output_image_dir,
                                "plate_" + str(filename).zfill(6) + "." + os.path.basename(filedir).split(".")[-1])
        txt_file = os.path.join(output_label_dir, "plate_" + str(filename).zfill(6) + ".txt")

        with open(txt_file, "w") as f:
            f.write(" ".join(["0", str(x), str(y), str(w), str(h)]))
        shutil.move(filedir, img_file)


def process_image(input_dir, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # 创建输出目录
    output_image_dir = os.path.join(output_dir, "images")
    output_label_dir = os.path.join(output_dir, "labels")

    images = find_images(input_dir)

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for filedir, filename in tqdm(images):
            future = executor.submit(work_process, filedir, filename, output_image_dir, output_label_dir)
            futures.append(future)

        for future in tqdm(futures):
            future.result()


if __name__ == "__main__":
    data_path = r"C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019\\ccpd_weather"
    save_path = r"C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019_YOLO\\ccpd_weather"

    process_image(input_dir=data_path, output_dir=save_path)
