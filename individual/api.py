"""
api.py
Indy Lyness
4/21/25

API style implementation for the CLI style script made for the previous assignment. Takes advantage of flask
to use URLs to replace command line arguments. Adapted from Jeff Ondich's flask_sample.py
"""

import flask
import csv
import json
import argparse

app = flask.Flask(__name__)

def convert_time(time):
    """
    Convert time string to integer representing seconds for comparison.
    """
    if time == '':
        return
    if ':' in time:
        sep = time.split(':')
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
    if 'm' in mark:
        return float(mark[:-1])
    elif '\'' in mark:
        sep = mark.split('\'')
        feet = int(sep[0])
        inches = float(sep[1][:-1])
        return 12*feet + inches
    else:
        return int(mark)

with open('../data/MIAC_data.csv') as csvfile:
    data = []
    reader = csv.reader(csvfile,  delimiter=',')
    header = reader.__next__()
    for row in reader:
        row_vals = {}
        for i, val in enumerate(row):
            row_vals[header[i]] = val
        data.append(row_vals)

# Get relevant column for each event (Time, Mark, Points)
events = set(row['Event'] for row in data)
event_key = {}
formats = ['Time', 'Mark', 'Points']
for event in events:
    event_performances = list(filter(lambda x: x['Event']==event, data))
    for format in formats:
        if event_performances[0][format] != '':
            event_key[event] = format

# Label each event with which column matters for result, then convert data from string to numeric format
for row in data:
    row['Result'] = event_key[row['Event']]
    row['Mark'] = convert_mark(row['Mark'])
    row['Conv'] = convert_mark(row['Conv'])
    row['Time'] = convert_time(row['Time'])
    row['Points'] = int(row['Points']) if row['Points'] != '' else None


@app.route('/help')
def get_help():
    return flask.render_template('help.html')

@app.route('/<gender>/<event_id>')
def get_performances(gender, event_id):
    performances = list(filter(lambda x: (x['Event']==event_id and x['Category']==gender), data))
    if event_key[event_id] == 'Time':
        performances.sort(key=lambda x:x[event_key[event_id]])
    else:
        performances.sort(key=lambda x:x[event_key[event_id]], reverse=True)
    lower = flask.request.args.get('lower')
    upper = flask.request.args.get('upper')
    unique = flask.request.args.get('unique', type=bool)
    conversion = flask.request.args.get('conversion', type=bool)

    if unique:
        athletes = set()
        best_performances = []
        for row in performances:
            if row["Athlete"] not in athletes:
                athletes.add(row["Athlete"])
                best_performances.append(row)
        performances = best_performances


    if event_key[event_id] == 'Time':
        if lower:
            performances = list(filter(lambda x: x['Time'] > convert_time(lower), performances))
        if upper:
            performances = list(filter(lambda x: x['Time'] < convert_time(upper), performances))
    else:
        if lower:
            if conversion:
                performances = list(filter(lambda x: x['Conv'] > convert_mark(lower), performances))
            else:
                performances = list(filter(lambda x: x[event_key[event_id]] > convert_mark(lower), performances))
        if upper:
            if conversion:
                performances = list(filter(lambda x: x['Conv'] < convert_mark(upper), performances))
            else:
                performances = list(filter(lambda x: x[event_key[event_id]] < convert_mark(upper), performances))
    

    return json.dumps(performances, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Flask API implementation of CLI assigment')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)