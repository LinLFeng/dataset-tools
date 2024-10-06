import time
from utils.log import normal_log, process_log


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
                statistics = f"[done {self._data_idx}] / [total {len(self._data)}]"
                process_log(self._text, statistics, end="", flush=True)
            return item
        else:
            # 结束后确保是 100%
            statistics = f"[done {len(self._data)}] / [total {len(self._data)}]"
            process_log(self._text, statistics, flush=True)
            raise StopIteration()
