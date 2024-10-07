import time
from utils.log import log


class Progress:
    def __init__(self, data, module="progress", title="progress", level=0):
        # 可迭代数据
        self._data = data
        # 索引
        self._data_idx = 0
        # 所在模块
        self._module = module
        # 进度标题
        self._title = title
        # 进度更新时间
        self._last_update = time.time()
        # 进度等级
        self._level = level

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
                statistics = f"{self._title} [done {self._data_idx}] / [total {len(self._data)}]"
                log(module=self._module,
                    msg=statistics,
                    flush=True,
                    level=self._level,
                    end="")
            return item
        else:
            # 结束后确保是 100%
            statistics = f"{self._title} [done {len(self._data)}] / [total {len(self._data)}]"
            log(module=self._module,
                msg=statistics,
                flush=True,
                level=self._level)
            raise StopIteration()
