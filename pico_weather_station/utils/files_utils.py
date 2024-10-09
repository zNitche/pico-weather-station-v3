import os


def check_if_exists(path: str):
    found = False

    try:
        os.stat(path)
        found = True

    except OSError:
        pass

    return found


def create_dir_if_doesnt_exit(dir_path: str):
    if not check_if_exists(dir_path):
        os.mkdir(dir_path)
