import os


def check_if_exists(path: str):
    try:
        os.stat(path)
        return True

    except OSError:
        pass

    return False


def create_dir_if_doesnt_exit(dir_path: str):
    if not check_if_exists(dir_path):
        os.mkdir(dir_path)
