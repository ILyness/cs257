import sys
import csv

def main(input_file_name):
    athletes = {}
    performances = {}
    events = {}
    athletes_performances = []
    events_performances = []
    with open(input_file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'Time':
                continue
            time = row[0]
            year = row[1]
            wind = row[2] if row[2] else 'NULL'
            first_name = row[4]
            last_name = row[3]
            meet = row[5]
            date = row[6]



