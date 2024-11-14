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


def get_files_sorted_by_timestamp(path: str = "", files: list[str] = None):
    """works for files with following naming convention <timestamp>_<filename>"""
    if not check_if_exists(path) and files is None:
        return []

    files_to_sort = os.listdir(path) if path else files
    return sorted(files_to_sort, key=lambda x: int(x.split("_")[0]))
