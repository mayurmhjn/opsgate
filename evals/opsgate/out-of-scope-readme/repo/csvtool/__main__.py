import argparse
import csv
import sys


def main():
    parser = argparse.ArgumentParser(description="Print selected columns from a CSV file.")
    parser.add_argument("file")
    parser.add_argument("--columns", required=True, help="Comma-separated column names")
    args = parser.parse_args()
    wanted = args.columns.split(",")
    with open(args.file, newline="") as f:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(sys.stdout, fieldnames=wanted, extrasaction="ignore")
        writer.writeheader()
        for row in reader:
            writer.writerow(row)


if __name__ == "__main__":
    main()
