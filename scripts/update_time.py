import argparse
import requests
from datetime import datetime


def main(args: argparse.Namespace):
    ip_address: str = args.address
    current_iso_datetime = datetime.now().isoformat()

    print(f"setting {ip_address} rtc datetime to {current_iso_datetime}...")

    body = {"datetime": current_iso_datetime}
    response = requests.post(f"{ip_address}/api/settings/set-date", json=body, timeout=5)

    print("got response")
    print(response.text)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--address",
        type=str,
        required=True,
        help="ip address of station, for example http://192.168.4.1",
    )

    return parser.parse_args()

if __name__ == '__main__':
    main(args=get_args())
