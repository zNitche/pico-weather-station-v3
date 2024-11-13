from pico_weather_station.utils import machine_utils


def init_csv_file(file_path: str, header: list[str]):
    with open(file_path, "w") as file:
        file.write(",".join(header) + "\n")


def write_row(file_path: str, row: str):
    with open(file_path, "a") as file:
        file.write(row + "\n")


def get_header(file_path: str):
    header = None

    with open(file_path, "r") as file:
        row = file.readline().replace("\n", "")

        if row:
            header = row.split(",")

    return header


def parse_row(row: str, header: list[str]):
    split_row = row.replace("\n", "").split(",")
    parsed_row = {}

    for index, header_item in enumerate(header):
        parsed_row[header_item] = split_row[index]

    return parsed_row


def get_csv_content(file_path: str, skip: int = 0, limit: int = 0):
    machine_utils.reset_heap()

    content = []
    header = get_header(file_path)

    if header:
        with open(file_path, "r") as file:
            for id, row in enumerate(file):
                if id > 0 + skip:
                    content.append(parse_row(row, header))

                    if 0 < limit <= len(content):
                        break

    return content


def get_rows_count(file_path: str):
    rows_count = 0

    with open(file_path, "r") as file:
        for _ in file:
            rows_count += 1

    if rows_count >= 1:
        rows_count -= 1

    return rows_count
