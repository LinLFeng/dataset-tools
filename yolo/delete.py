import os
import re
from tqdm import tqdm

root_path = "C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019_YOLO\\ccpd_base"

# 图片名列表
images = dict()
images_index = []

# 标签名列表
labels = dict()
labels_index = []

for i in tqdm(os.listdir(os.path.join(root_path, "images"))):
    index = int(re.findall(r"_(\d+)", i)[0])
    images[index] = i.rsplit(".", 1)[0]
    images_index.append(index)

for i in tqdm(os.listdir(os.path.join(root_path, "labels"))):
    index = int(re.findall(r"_(\d+)", i)[0])
    labels[index] = i.rsplit(".", 1)[0]
    labels_index.append(index)

inters1 = list(set(images_index) - set(labels_index))
inters2 = list(set(labels_index) - set(images_index))

for i in tqdm(inters1):
    file_name = "images\\" + images[i] + ".jpg"
    os.remove(os.path.join(root_path, file_name))

for i in tqdm(inters2):
    file_name = "labels\\" + labels[i] + ".txt"
    os.remove(os.path.join(root_path, file_name))


def delete_files(num):
    print(f"delete num {num}")
    for i in tqdm(images_index):
        if i > num:
            file_name1 = "images\\" + images[i] + ".jpg"
            file_name2 = "labels\\" + labels[i] + ".txt"
            os.remove(os.path.join(root_path, file_name1))
            os.remove(os.path.join(root_path, file_name2))


delete_files(20000)

print("Done.")
