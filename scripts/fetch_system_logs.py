import argparse
import os
import requests


def main(args: argparse.Namespace):
    ip_address: str = args.address
    output_dir: str = args.out

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    base_url = f"{ip_address}/api/logs"

    print(f"getting logs list from {ip_address}...")
    response = requests.get(base_url, timeout=5)
    logs_list = response.json().get("logs")

    print(f"logs list: {logs_list}")

    for log in logs_list:
        print(f"processing {log}")
        response = requests.get(f"{base_url}/{log}", timeout=5)

        with open(os.path.join(output_dir, f"{log}.txt"), "w") as file:
            file.write(response.text)

        print(f"done...")


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--address",
        type=str,
        required=True,
        help="ip address of station, for example http://192.168.4.1",
    )

    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="path to output directory",
    )

    return parser.parse_args()

if __name__ == '__main__':
    main(args=get_args())
