import argparse
import datetime
import json
import re
from pathlib import Path

PATH = Path(__file__).resolve().parent / "stats.json"

def delete(path: Path) -> None:
    if not path.exists():
        return
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

def list_(path: Path) -> tuple:
    if path.exists():
        with open(path, "r") as file:
            data = json.load(file)
        day = data[-1]["Day"] + 1 
        total_time = data[-1]["Total Time"]
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

def to_hour_format(time: str):
    day, hour, minutes, seconds = parse_time(time)
    return f"{day * 24 + hour}:{minutes}:{seconds}"

def on(path: Path) -> None:
    
    day, total_time = list_(path)
    data = {
        "Day": day,
        "Date": datetime.datetime.now().replace(microsecond=0).isoformat(),
        "Time": "00:00:00",
        "Total Time": total_time,
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
    if not path.exists():
        return

    with open(path, "r") as file:
        data = json.load(file)

    date_str = data[-1]["Date"]
    time_ = datetime.datetime.now() - datetime.datetime.fromisoformat(date_str)
    total_time_str = data[-1]["Total Time"]

    d, h, m, s = parse_time(total_time_str)
    
    total_time = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s) + time_

    total_time_str = str(total_time).split(".")[0]

    data[-1]["Time"] = str(time_).split(".")[0]
    data[-1]["Total Time"] = to_hour_format(total_time_str)
    data[-1]["Notes"] = notes if notes else ""

    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--on", action="store_true", help="Turn the program on")
    parser.add_argument("--off", action="store_true", help="Turn the program off")
    parser.add_argument("-l","--last", action="store_true", help="Show the last record")
    parser.add_argument("-f", "--first", action="store_true", help="Show the first record")
    parser.add_argument("-d","--delete", action="store_true", help="Delete all records")
    parser.add_argument("-n", "--notes", type=str, help="Notes can only be added when turning the program off")
    args = parser.parse_args()

    if args.on:
        on(PATH)
    if args.off:
        off(PATH, args.notes)
    if args.last:
        last(PATH)
    if args.first:
        first(PATH)
    if args.delete:
        delete(PATH)