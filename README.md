# 数据集处理工具

## 1 基础介绍

### 项目目标

部分数据集由于格式原因  
无法直接被深度学习框架的DataLoader直接读取  
而自行编写DataLoader过于复杂  
故编写该工具  
实现数据格式之间的快速转换等功能

### 项目介绍

- convert 数据转换功能模块
    - ccpd.py
        - CCPD2019数据集 生成 yolo标签 ocr标签
    - dataset_cut.py
        - 以目录分类的数据集 生成 train/val/test_list.txt

- generate 生成功能模块 
    - multi_categorization.py
        - 以目录分类的数据集 生成 train/val/test_list.txt

- utils 工具集模块

    - fileloader.py 文件加载功能
    - progress.py 进度显示功能

## 2 快速使用

！！！开始先请注意！！！  
该工具部分功能是对原始数据集直接修改  
因此该数据集若有其他需求请一定做好备份

### 环境搭建

python3.x 版本  
目前没有引入第三方库

### 运行

修改 convert/你需要的功能.py 中的参数  
修改后直接运行即可


