import time


class Progress:
    def __init__(self, data, text="progress"):
        # 可迭代数据
        self.data = data
        # 索引
        self.data_idx = 0
        # 进度标题
        self.text = text
        # 进度更新时间
        self.last_update = time.time()

    def __iter__(self):
        return self

    def __next__(self):
        if self.data_idx < len(self.data):
            item = self.data[self.data_idx]
            self.data_idx += 1
            now = time.time()
            if now - self.last_update > 0.3:
                # 更新时间
                self.last_update = now
                # 计算比例
                progress = (self.data_idx / len(self.data)) * 100
                print(f"\r{self.text} - {progress:.2f}%", end="", flush=True)
            return item
        else:
            # 结束后确保是 100%
            print(f"\r{self.text} - 100.00%", end="\n", flush=True)
            raise StopIteration()
