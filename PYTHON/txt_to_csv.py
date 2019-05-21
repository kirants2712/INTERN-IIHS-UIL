import csv
import pandas as pd

with open('<name of the file>.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split("|") for line in stripped if line)
    with open('<name of output file>.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
