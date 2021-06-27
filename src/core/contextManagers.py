from contextlib import contextmanager


@contextmanager
def open_dataset(file: str, mode: str = "r"):
    f = open(file, mode)
    try:
        yield f
    finally:
        f.close()
