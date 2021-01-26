import os


def get_filesize(path):
    size = os.path.getsize(path)
    return round(size / (1024 * 1024), 3)