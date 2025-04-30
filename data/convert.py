"""
Convert.py
Soren Kaster, Indy Lyness, Daniel Scheider
4/29/25

Script to convert MIAC_data_final.csv (or a csv file matching its format) into smaller csv files to
upload into an SQL database. Those files are:

    - 
"""


import sys
import csv

def main(input_file_name):
    athletes = {}
    performances = {}
    events = {}
    athletes_performances = []
    with open(input_file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'Time':
                continue
            time = row[0] if row[0] else 'NULL'
            # year = row[1] if row[1] else 'NULL'
            wind = row[2] if row[2] else 'NULL'
            first_name = row[4] if row[4] else 'NULL'
            last_name = row[3] if row[3] else 'NULL'
            meet = row[5]
            date = row[6]
            event = row[7]
            season = row[8]
            relay = row[9] if row[9] else 'NULL'
            mark = row[10] if row[10] else 'NULL'
            school = row[11]
            category = row[12]
            points = row[13] if row[13] else 'NULL'
            if first_name != 'NULL':
                athlete_key = f'{first_name}+{last_name}'
                if athlete_key not in athletes:
                    athletes[athlete_key] = {'id': len(athletes),
                                             'first_name': first_name,
                                             'last_name': last_name,
                                             'school': school,
                                             'gender': category}
            event_key = f'{event}+{season.split()[0]}'
            if event_key not in events:
                if time != 'NULL': 
                    event_category = 'Running'
                elif points != 'NULL':
                    event_category = 'Multi'
                else:
                    event_category = 'Field'
                events[event_key] = {'id': len(events),
                                     'event': event,
                                     'event_category': event_category,
                                     'season_category': season.split()[0]}
                
            if time != 'NULL':
                performance_key = f'{last_name}+{event}+{date}'
                result = time
            elif points != 'NULL':
                performance_key = f'{last_name}+{event}+{date}'
                result = points
            else:
                performance_key = f'{last_name}+{event}+{date}+{mark}'
                result = mark

            performances[performance_key] = {'id': len(performances),
                                             'mark': result,
                                             'wind': wind,
                                             'result_date': date,
                                             'meet': meet,
                                             'season': season,
                                             'event_id': events[event_key]['id']}
            if relay == 'NULL':
                athletes_performances.append((athletes[athlete_key]['id'],performances[performance_key]['id']))
            else:
                relay_team = relay.split(',')
                for leg in relay_team:
                    for athlete_key in athletes:
                        if athletes[athlete_key]['last_name'] == leg and athletes[athlete_key]['school'] == school:
                            athletes_performances.append((athletes[athlete_key]['id'],performances[performance_key]['id']))

    with open('athletes.csv', 'w') as f:
        writer = csv.writer(f)
        for athlete_key in athletes:
            athlete = athletes[athlete_key]
            row = (athlete['id'], athlete['first_name'], athlete['last_name'], athlete['school'], athlete['gender'])
            writer.writerow(row)

    with open('events.csv', 'w') as f:
        writer = csv.writer(f)
        for event_key in events:
            event = events[event_key]
            row = (event['id'], event['event'], event['event_category'], event['season_category'])
            writer.writerow(row)

    with open('performances.csv', 'w') as f:
        writer = csv.writer(f)
        for performance_key in performances:
            performance = performances[performance_key]
            row = (performance['id'], performance['mark'], performance['wind'], performance['result_date'], performance['meet'], performance['season'], performance['event_id'])
            writer.writerow(row)

    with open('athletes_performances.csv', 'w') as f:
        writer = csv.writer(f)
        for athlete_id, performance_id in athletes_performances:
            writer.writerow((athlete_id, performance_id))

                    
if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} original_csv_file', file=sys.stderr)
    exit()

main(sys.argv[1])