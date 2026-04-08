import argparse
import datetime
import json
import re
from pathlib import Path

STATS_PATH = Path(__file__).resolve().parent / "stats.json"


def list_(path: Path) -> tuple:
    if path.exists():
        with open(path, "r") as file:
            data = json.load(file)
        day = data[-1]["Day"] + 1
        total_time = data[-1]["Total time"]
        return day, total_time
    else:
        day = 1
        total_time = "00:00:00"
        return day, total_time


def parse_time(time: str) -> tuple:
    pattern = re.compile(
        r"^(?:(?P<day>\d+)\s+days?,\s*)?"
        r"(?P<hours>\d+):"
        r"(?P<minutes>\d+):"
        r"(?P<seconds>\d+)$"
    )

    m = pattern.match(time)
    data = m.groupdict()

    day = int(data["day"] or 0)
    hours = int(data["hours"])
    minutes = int(data["minutes"])
    seconds = int(data["seconds"])

    return day, hours, minutes, seconds


def status(path: Path) -> str:
    with open(path, "r") as file:
        data = json.load(file)

    return data[-1]["Stop status"]


def to_hour_format(time: str):
    day, hour, minutes, seconds = parse_time(time)
    return f"{day * 24 + hour}:{minutes}:{seconds}"


def delete_all(path: Path) -> None:
    if not path.exists():
        return
    path.unlink()


def delete_last(path: Path) -> None:
    if not path.exists():
        return

    with open(path, "r") as file:
        data = json.load(file)

    if data:
        del data[-1]
        if data:
            with open(path, "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            path.unlink()


def last(path: Path) -> None:
    if not path.exists():
        return
    with open(path, "r") as file:
        data = json.load(file)
    print(data[-1])


def first(path: Path) -> None:
    if not path.exists():
        return
    with open(path, "r") as file:
        data = json.load(file)
    print(data[0])


def on(path: Path) -> None:
    day, total_time = list_(path)
    data = {
        "Day": day,
        "Date": datetime.datetime.now().replace(microsecond=0).isoformat(),
        "Stop time": "00:00:00",
        "Start time": "00:00:00",
        "Start / Stop time": "00:00:00",
        "Stop status": False,
        "Time": "00:00:00",
        "Finish time": "00:00:00",
        "Total time": total_time,
        "Notes": ""
    }

    if path.exists():
        with open(path, "r") as file:
            items = json.load(file)
    else:
        items = []

    items.append(data)
    with open(path, "w") as file:
        json.dump(items, file, ensure_ascii=False, indent=4)


def off(path: Path, notes: str) -> None:
    stop_status = status(path)

    if stop_status:
        return

    if not path.exists():
        return

    with open(path, "r") as file:
        data = json.load(file)

    date_str = data[-1]["Date"]
    time_ = datetime.datetime.now() - datetime.datetime.fromisoformat(date_str)

    start_stop_time_str = data[-1]["Start / Stop time"]
    d, h, m, s = parse_time(start_stop_time_str)
    new_time = time_ - datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)

    total_time_str = data[-1]["Total time"]
    d, h, m, s = parse_time(total_time_str)
    total_time = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s) + new_time

    total_time_str = str(total_time).split(".")[0]

    data[-1]["Start / Stop time"] = str(start_stop_time_str).split(".")[0]
    data[-1]["Time"] = str(new_time).split(".")[0]
    data[-1]["Finish time"] = datetime.datetime.now().isoformat()
    data[-1]["Total time"] = to_hour_format(total_time_str)

    data[-1]["Notes"] = notes if notes else ""

    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def stop(path: Path) -> None:
    stop_status = status(path)

    if stop_status:
        return

    stop_status = True

    with open(path, "r") as file:
        data = json.load(file)

    data[-1]["Stop time"] = datetime.datetime.now().isoformat()
    data[-1]["Stop status"] = stop_status

    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def start(path: Path) -> None:
    stop_status = status(path)

    if not stop_status:
        return

    stop_status = False

    with open(path, "r") as file:
        data = json.load(file)

    start_stop_time_str = data[-1]["Start / Stop time"]
    d, h, m, s = parse_time(start_stop_time_str)

    start_time = datetime.datetime.now()
    stop_time = datetime.datetime.fromisoformat(data[-1]["Stop time"])
    time_start_stop = (
        start_time
        - stop_time
        + datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
    )

    data[-1]["Start time"] = start_time.isoformat()
    data[-1]["Start / Stop time"] = str(time_start_stop).split(".")[0]
    data[-1]["Stop status"] = stop_status

    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--on", action="store_true", help="Turn the program on")
    parser.add_argument("--off", action="store_true", help="Turn the program off")
    parser.add_argument(
        "-l", "--last", action="store_true", help="Show the last record"
    )
    parser.add_argument(
        "-f", "--first", action="store_true", help="Show the first record"
    )
    parser.add_argument(
        "-da", "--delete-all", action="store_true", help="Delete all records"
    )
    parser.add_argument(
        "-dl", "--delete-last", action="store_true", help="Delete last record"
    )
    parser.add_argument(
        "-n",
        "--notes",
        type=str,
        help="Notes can only be added when turning the program off",
    )
    parser.add_argument("--stop", action="store_true", help="Stop your time")
    parser.add_argument("--start", action="store_true", help="Start your time")
    args = parser.parse_args()

    if args.on:
        on(STATS_PATH)
    if args.off:
        off(STATS_PATH, args.notes)
    if args.stop:
        stop(STATS_PATH)
    if args.start:
        start(STATS_PATH)
    if args.last:
        last(STATS_PATH)
    if args.first:
        first(STATS_PATH)
    if args.delete_all:
        delete_all(STATS_PATH)
    if args.delete_last:
        delete_last(STATS_PATH)
