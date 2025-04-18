"""
cli.py
Indy Lyness
4/17/24

NAME: cli.py - command line interface exercise
SYNOPSIS: python3 cli.py event gender 
DESCRIPTION: Return the first specified number of performances that 
are better than a specified cutoff for a specified event.
"""

import argparse
import csv 

def get_parsed_arguments():
    """
    Get command line arguments. Any cutoff provided must follow a strict format - see help.
    """
    parser = argparse.ArgumentParser(description='Filter performances based on event and time/mark.')
    parser.add_argument('event', help='Event that you would like to filter for. Examples: \"400 Meters\", \"Shot Put\", etc.')
    parser.add_argument('gender', help='Gender to filter for. Options are \'m\' for men and \'f\' for women.')
    parser.add_argument('--cutoff', '-c', help='Optional cutoff to filter performances by. For running events, this should be a time (mm:ss.xx), and for field events this should be a mark (12.37m or 4\' 2.5\").')
    parser.add_argument('--conv', action='store_true', help='Whether to recognize the cutoff mark as feet\' inches\" format (default is meters - if you put feet/inches format and do not specify this flag you will get an error).')
    parser.add_argument('--number', '-n', default=10, help='Number of performances to display (displays all performances if there are less than the given number after filtering).')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def convert_time(time):
    """
    Convert time string to integer representing seconds for comparison.
    """
    if time == '':
        return
    if ":" in time:
        sep = time.split(":")
        mins = int(sep[0])
        secs = float(sep[1])
        return mins*60 + secs
    else:
        secs = float(time)
        return secs
    
def convert_mark(mark):
    """
    Convert mark for field event to numeric - units are context dependent.
    """
    if mark == '':
        return
    if "m" in mark:
        return float(mark[:-1])
    sep = mark.split('\'')
    feet = int(sep[0])
    inches = float(sep[1][:-1])
    return 12*feet + inches

def display_performances(performances, format):
    """
    Print performances that match filter in table format.
    """
    if performances == []:
        print("No performances matching filter.")
        return
    type = performances[0]["Result"]
    header = "Athlete".ljust(20) + "| Year".ljust(8) + "| School".ljust(20) + "| Event".ljust(15) + f"| {format}".ljust(10) + "| Date".ljust(15) + "| Meet".ljust(20)
    print(header)
    print("-"*150)
    for row in performances:
        if type == "Time":
            mins = row["Time"] // 60
            secs = row["Time"] % 60
            if mins > 0:
                result_string = f"{mins:.0f}:{secs:.2f}"
            else:
                result_string = f"{secs:.2f}"
        elif format == False:
            result_string = f"{row["Mark"]}m"
        else:
            feet = row["Conv"] // 12
            inches = row["Conv"] % 12
            result_string = f"{feet:.0f}\'{inches:.2f}\""
        display = f"{row['Athlete']}".ljust(20) + f"| {row['Year']}".ljust(8) + f"| {row['School']}".ljust(20) + f"| {row['Event']}".ljust(15) + result_string.ljust(10) + f"| {row['Meet Date']}".ljust(15) + f"| {row['Meet']}".ljust(20)
        print(display)
        print("-"*150)

def get_performances(arguments):
    """
    Find performances that match filters provided. Loads data, then creates a list of dictionary objects to represent the rows. Data can then be
    sorted by accessing different keys for each entry.
    """

    # Set up list-dictionary data structure
    with open("MIAC_data.csv") as csvfile:
        data = []
        reader = csv.reader(csvfile,  delimiter=',')
        header = reader.__next__()
        for row in reader:
            row_vals = {}
            for i, val in enumerate(row):
                row_vals[header[i]] = val
            data.append(row_vals)

    # Get relevant column for each event (Time, Mark, Points)
    events = set(row["Event"] for row in data)
    event_key = {}
    formats = ["Time", "Mark", "Points"]
    for event in events:
        event_performances = list(filter(lambda x: x["Event"]==event, data))
        for format in formats:
            if event_performances[0][format] != '':
                event_key[event] = format
    
    # Label each event with which column matters for result, then convert data from string to numeric format
    for row in data:
        row["Result"] = event_key[row["Event"]]
        row["Mark"] = convert_mark(row["Mark"])
        row["Conv"] = convert_mark(row["Conv"])
        row["Time"] = convert_time(row["Time"])

    # Filter by gender
    if arguments.gender == "m":
        data = list(filter(lambda x: x["Category"]=='m', data))
    else:
        data = list(filter(lambda x: x["Category"]=='f', data))

    # Filter by event and optional cutoff using standard filter function and relevant dictionary key
    if event_key[arguments.event] == "Time":
        performances = list(filter(lambda x: x["Event"]==arguments.event, data))
        performances.sort(key=lambda x:x["Time"])
        performances = performances[:int(arguments.number)]
        if arguments.cutoff:
            performances = list(filter(lambda x: x["Time"] < convert_time(arguments.cutoff), performances))
    else:
        performances = list(filter(lambda x: x["Event"]==arguments.event, data))
        performances.sort(key=lambda x:x["Mark"], reverse=True)
        performances = performances[:int(arguments.number)]
        if arguments.cutoff:
            if arguments.conv:
                performances = list(filter(lambda x: x["Conv"] > convert_mark(arguments.cutoff), performances))
            else:
                performances = list(filter(lambda x: x["Mark"] > convert_mark(arguments.cutoff), performances))

    return performances

def main():
    arguments = get_parsed_arguments()
    performances = get_performances(arguments)
    display_performances(performances, arguments.conv)

if __name__ == "__main__":
    main()

