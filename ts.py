#!/usr/bin/env python3
import argparse
import datetime
import sys


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-f", "--format", type=str,
                        help="Output datetime format (strftime)")
    group.add_argument("-i", action="store_true",
                       help="Set time field to the interval between lines")
    group.add_argument("-s", action="store_true",
                       help="Set time field to the interval from start")
    args = parser.parse_args()

    if not args.format:
        if args.i or args.s:
            # not actualy used because timedelta has no strftime
            # so for now for intervals, just support %S and %S.%f
            # and the default output of timedelta matches below
            args.format = "%H:%M:%S.%f"
    args.format = args.format or "%Y-%m-%d %H:%M:%S.%f"

    start_time = last_time = datetime.datetime.now()
    for line in sys.stdin:
        now = datetime.datetime.now()
        if args.i:
            dt = now - last_time
        elif args.s:
            dt = now - start_time
        else:
            dt = now.strftime(args.format)
        if (args.i or args.s):
            if args.format == "%S":
                dt = f"{int(dt.total_seconds())}"
            elif args.format == "%S.%f":
                dt = f"{dt.total_seconds():.6f}"
        sys.stdout.write(f"{dt} {line}")
        last_time = now


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
