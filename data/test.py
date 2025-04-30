import csv

with open('performances.csv', 'r') as f:
    reader = csv.reader(f)
    j = 0
    for i, row in enumerate(reader):
        if i != int(row[0]):
            j += 1
    print(f'There are {j} collisions in performance ids')