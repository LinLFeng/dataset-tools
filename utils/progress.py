import time


class Progress:
    def __init__(self, data, text="progress"):
        # 可迭代数据
        self._data = data
        # 索引
        self._data_idx = 0
        # 进度标题
        self._text = text
        # 进度更新时间
        self._last_update = time.time()

    def __iter__(self):
        return self

    def __next__(self):
        if self._data_idx < len(self._data):
            item = self._data[self._data_idx]
            self._data_idx += 1
            now = time.time()
            if now - self._last_update > 0.3:
                # 更新时间
                self._last_update = now
                # 计算比例
                statistics = f"[{self._text} - [done {self._data_idx}] / [total {len(self._data)}]]"
                print(f"\r{statistics}", end="", flush=True)
            return item
        else:
            # 结束后确保是 100%
            statistics = f"[{self._text} - [done {len(self._data)}] / [total {len(self._data)}]] Done"
            print(f"\r{statistics}", end="\n", flush=True)
            raise StopIteration()
