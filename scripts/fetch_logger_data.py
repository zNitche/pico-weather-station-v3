import argparse
import os
import requests


def fetch(url: str,
          data_key: str | None = None,
          raw: bool = False) -> dict[str, ...] | list[any] | None | str:
    response = requests.get(url, timeout=7)

    if not raw:
        json = response.json()
        return json if data_key is None else json.get(data_key)

    else:
        return response.text


def check_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def filter_date_items(input: list[str], value: str | None) -> list[str]:
    return [value] if value in input else []


def main(args: argparse.Namespace):
    ip_address: str = args.address
    logger_name: str = args.logger
    output_dir: str = args.out
    target_year: str | None = args.year
    target_month: str | None = args.month

    base_url = f"{ip_address}/api/data-logs"

    print(f"getting list of available loggers from {ip_address}...")
    loggers_list = fetch(url=f"{base_url}/loggers", data_key="loggers")

    print(f"available loggers: {loggers_list}")

    if logger_name in loggers_list:
        print(f"processing {logger_name}...")
        years = fetch(url=f"{base_url}/logs/{logger_name}/years", data_key="years")

        print(f"logged years: {years}")

        if target_year is not None:
            print(f"filtering year: {target_year}")
            years = filter_date_items(years, target_year)

        for year in years:
            print(f"processing {year}")
            months = fetch(url=f"{base_url}/date/{logger_name}/{year}", data_key="months")

            print(f"got following months: {months}")

            if target_month is not None:
                print(f"filtering month: {target_month}")
                months = filter_date_items(months, target_month)

            for month in months:
                print(f"processing {month}/{year}...")
                days = fetch(url=f"{base_url}/date/{logger_name}/{year}/{month}", data_key="days")

                print(f"got logged days for {month}/{year} : {days}")

                out_dir = os.path.join(output_dir, str(year), str(month))
                check_dir(out_dir)

                for day in days:
                    print(f"processing {day}/{month}/{year}...")
                    data = fetch(url=f"{base_url}/date/{logger_name}/{year}/{month}/{day}?raw=1", raw=True)

                    print("saving data...")

                    with open(os.path.join(out_dir, f"{day}.txt"), "w") as file:
                        file.write(data)

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

    parser.add_argument(
        "--logger",
        type=str,
        required=True,
        help="logger name",
    )

    parser.add_argument(
        "--year",
        type=str,
        default=None,
        help="year to fetch logs for, for example 2025",
    )

    parser.add_argument(
        "--month",
        type=str,
        default=None,
        help="month to fetch logs for, for example 2025",
    )

    return parser.parse_args()

if __name__ == '__main__':
    main(args=get_args())
