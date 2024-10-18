import os


def check_if_exists(path: str):
    try:
        os.stat(path)
        return True

    except OSError:
        pass

    return False


def create_dir_if_doesnt_exist(dir_path: str):
    if not check_if_exists(dir_path):
        path = ""
        path_parts = dir_path.split("/")

        for part in path_parts:
            if part:
                path += f"/{part}"

                if not check_if_exists(path):
                    os.mkdir(path)
