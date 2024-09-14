import os  
import os.path  
import re  
import shutil  
import cv2  
from tqdm import tqdm  
from concurrent.futures import ThreadPoolExecutor  
  
  
def listPathAllfiles(dirname):  
    result = []  
    for maindir, subdir, file_name_list in os.walk(dirname):  
        for filename in file_name_list:  
            apath = os.path.join(maindir, filename)  
            result.append(apath)  
    return result  
  
  
def process_image(name, images_save_path, labels_save_path, cnt):  
    if name.endswith(".jpg") or name.endswith(".png"):  
        img = cv2.imread(name)  
        height, width = img.shape[0], img.shape[1]  
  
        str1 = re.findall("-\d+\&\d+_\d+\&\d+-", name)[0][1:-1]  
        str2 = re.split("\&|_", str1)  
        x0, y0, x1, y1 = map(int, str2)  
  
        x = round((x0 + x1) / 2 / width, 6)  
        y = round((y0 + y1) / 2 / height, 6)  
        w = round((x1 - x0) / width, 6)  
        h = round((y1 - y0) / height, 6)  
  
        txtfile = os.path.join(labels_save_path, "plate_" + str(cnt).zfill(6) + ".txt")  
        imgfile = os.path.join(images_save_path, "plate_" + str(cnt).zfill(6) + "." + os.path.basename(name).split(".")[-1])  
  
        with open(txtfile, "w") as f:  
            f.write(" ".join(["0", str(x), str(y), str(w), str(h)]))  
        shutil.move(name, imgfile)  
  
  
if __name__ == "__main__":  
    data_path = r"C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019\\ccpd_weather"  
    save_path = r"C:\\Users\\LIN_L\\Project\\datasets\\CCPD2019_YOLO\\ccpd_weather"  
  
    images_save_path = os.path.join(save_path, "images")  
    labels_save_path = os.path.join(save_path, "labels")  
  
    os.makedirs(images_save_path, exist_ok=True)  
    os.makedirs(labels_save_path, exist_ok=True)  
  
    images_files = listPathAllfiles(data_path)  
  
    with ThreadPoolExecutor(max_workers=50) as executor:  # 可以调整max_workers的数量  
        futures = []  
        for cnt, name in enumerate(tqdm(images_files), start=1):  
            future = executor.submit(process_image, name, images_save_path, labels_save_path, cnt)  
            futures.append(future)  
  
        # 等待所有任务完成  
        for future in tqdm(futures, desc="Processing images"):  
            future.result()