"""
cli.py
Indy Lyness
4/17/24

NAME: cli.py - command line interface exercise
SYNOPSIS: python3 cli.py event gender 
DESCRIPTION: Return performances filtered by an event and gender, with optional bounds on the time/mark.
The number of performances displayed and whethere there are multiple for each individual athlete can also be specified.
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
    parser.add_argument('--upper', '-p', help='Upper bound to filter performances by. For running events, this should be a time (mm:ss.xx), and for field events this should be a mark (12.37m or 4\' 2.5\"). For the decathlon, this should be a point value (e.g. 5000).')
    parser.add_argument('--lower', '-l', help='Lower bound to filter performances by. See --upper description for formatting notes.')
    parser.add_argument('--conv', action='store_true', help='Whether to recognize the cutoff mark as feet\' inches\" format (default is meters - if you put feet/inches format and do not specify this flag you will get an error).')
    parser.add_argument('--number', '-n', help='Maximum number of performances to display (displays all performances if there are less than the given number after filtering).')
    parser.add_argument('--unique', '-u', action='store_true', help='Whether to display just the best performance for each athlete.')
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
    elif '\'' in mark:
        sep = mark.split('\'')
        feet = int(sep[0])
        inches = float(sep[1][:-1])
        return 12*feet + inches
    else:
        return int(mark)

def display_performances(performances, format):
    """
    Print performances that match filter in table format.
    """
    if performances == []:
        print("No performances matching filter.")
        return
    type = performances[0]["Result"]
    header = "Athlete".ljust(25) + "| Year".ljust(8) + "| School".ljust(22) + "| Event".ljust(20) + f"| {type}".ljust(12) + "| Date".ljust(15) + "| Meet".ljust(20)
    print("-"*160)
    print(header)
    print("-"*160)
    for row in performances:
        if type == "Time":
            mins = row["Time"] // 60
            secs = row["Time"] % 60
            if mins > 0:
                result_string = f"{mins:02.0f}:{secs:05.2f}"
            else:
                result_string = f"{secs:05.2f}"
        elif type == "Mark":
            if format == False:
                result_string = f"{row["Mark"]}m"
            else:
                feet = row["Conv"] // 12
                inches = row["Conv"] % 12
                result_string = f"{feet:.0f}\'{inches:04.2f}\""
        else:
            result_string = row["Points"]
        display = f"{row['Athlete']}".ljust(25) + f"| {row['Year']}".ljust(8) + f"| {row['School']}".ljust(22) + f"| {row['Event']}".ljust(20) + f"| {result_string}".ljust(12) + f"| {row['Meet Date']}".ljust(15) + f"| {row['Meet']}".ljust(20)
        print(display)
        print("-"*160)

def get_performances(arguments):
    """
    Find performances that match filters provided. Loads data, then creates a list of dictionary objects to represent the rows. Data can then be
    sorted by accessing different keys for each entry.
    """

    # Set up list-dictionary data structure
    with open("data/MIAC_data.csv") as csvfile:
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
        row["Points"] = int(row["Points"]) if row["Points"] != "" else None

    # Filter by gender and event
    if arguments.gender == "m":
        data = list(filter(lambda x: x["Category"]=='m', data))
    else:
        data = list(filter(lambda x: x["Category"]=='f', data))

    performances = list(filter(lambda x: x["Event"]==arguments.event, data))

    # Filter for any bounds provided for time/mark
    if event_key[arguments.event] == "Time":
        performances.sort(key=lambda x:x[event_key[arguments.event]])
        if arguments.lower:
            performances = list(filter(lambda x: x["Time"] > convert_time(arguments.lower), performances))
        if arguments.upper:
            performances = list(filter(lambda x: x["Time"] < convert_time(arguments.upper), performances))
    else:
        performances.sort(key=lambda x:x[event_key[arguments.event]], reverse=True)
        if arguments.lower:
            if arguments.conv:
                performances = list(filter(lambda x: x["Conv"] > convert_mark(arguments.lower), performances))
            else:
                performances = list(filter(lambda x: x[event_key[arguments.event]] > convert_mark(arguments.lower), performances))
        if arguments.upper:
            if arguments.conv:
                performances = list(filter(lambda x: x["Conv"] < convert_mark(arguments.upper), performances))
            else:
                performances = list(filter(lambda x: x[event_key[arguments.upper]] < convert_mark(arguments.cutoff), performances))

    # Filter down to best performance for each athlete if specified
    if arguments.unique:
        athletes = set()
        final_performances = []
        for row in performances:
            if row["Athlete"] not in athletes:
                athletes.add(row["Athlete"])
                final_performances.append(row)
    else:
        final_performances = performances

    if arguments.number:
        final_performances = final_performances[:int(arguments.number)]
    

    return final_performances

def main():
    arguments = get_parsed_arguments()
    performances = get_performances(arguments)
    if arguments.number:
        num_performances = max(arguments.number, len(performances))
    else:
        num_performances = len(performances)
    print(f"{num_performances} Results")
    display_performances(performances, arguments.conv)

if __name__ == "__main__":
    main()

