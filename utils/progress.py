class Progress:
    def __init__(self, data, text="progress") -> None:
        self.data = data
        self.data_idx = 0
        self.data_len = len(data)
        self.text = text

    def __iter__(self):
        return self

    def __next__(self):
        if self.data_idx < self.data_len:
            ask = self.data[self.data_idx]
            self.data_idx += 1
            progress = (self.data_idx / self.data_len) * 100
            print(f"\r%s - %d%%" % (self.text, progress), end="")
            return ask
        else:
            print("")
            raise StopIteration()
