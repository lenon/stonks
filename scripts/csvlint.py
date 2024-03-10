#!/usr/bin/env python
import csv
import os
import sys

if len(sys.argv) < 2:
    print("error: must pass a file", file=sys.stderr)
    exit(1)

file = sys.argv[1]
tmpfile = f"{file}.tmp"

if not file or not os.path.isfile(file) or not os.access(file, os.R_OK):
    print(f"error: file {file} is not a readable file", file=sys.stderr)
    exit(1)


with open(file, newline="") as input, open(tmpfile, "w", newline="") as output:
    reader = csv.reader(input, delimiter=";")
    writer = csv.writer(output, delimiter=",", lineterminator="\n")

    writer.writerows(reader)

os.replace(tmpfile, file)
