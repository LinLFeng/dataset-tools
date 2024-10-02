import os


def file_loader(path):
    loop_rounds = -1
    data = dict()
    category = list()

    for filedir, subdir, file_name_list in os.walk(path):
        if len(subdir) == 0:
            return file_name_list
        else:
            if loop_rounds == -1:
                category = subdir
                loop_rounds += 1
            else:
                data[category[loop_rounds]] = file_name_list
                loop_rounds += 1

    return data
