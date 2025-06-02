"""
Convert.py
Soren Kaster, Indy Lyness, Daniel Scheider
4/29/25

Script to convert MIAC_data_final.csv (or a csv file matching its format) into smaller csv files to
upload into an SQL database. Those files are:

    - athletes.csv: id, last_name, first_name, gender
    - schools.csv: id, school_name
    - seasons.csv: id, season_name, season_category
    - events.csv: id, event_name, event_category, season_category
    - performances.csv: id, mark, wind, result_date
    - results.csv: athlete_id, performance_id, school_id, event_id, season_id, meet_id
    - meets.csv: id, meet_name, meet_date

    Adapted from Jeff Ondich's csv2tables.py from the course repository.
"""


import sys
import csv

def parse_time(t):  
    if ':' in t:
        minutes, seconds = t.split(':')
        return round(int(minutes) * 60 + float(seconds), 2)
    else:
        return round(float(t), 2)

def main(input_file_name):
    athletes = {}
    performances = {}
    events = {}
    seasons = {}
    schools = {}
    meets = {}
    results = []
    
    with open(input_file_name) as f:
        reader = csv.reader(f)
        headers = {}
        for row in reader:
            # Get all data values from row
            if len(headers) == 0:
                for i, col in enumerate(row):
                    headers[col] = i
                continue
            time = row[headers['Time']] if row[headers['Time']] else 'NULL'
            schoolYear = row[headers['Year']] if row[headers['Year']] else 'NULL'
            wind = row[headers['Wind']] if (row[headers['Wind']] and row[headers['Wind']] != 'NWI') else 'NULL'
            first_name = row[headers['First Name']].strip() if row[headers['First Name']] else 'NULL'
            last_name = row[headers['Last Name']].strip() if row[headers['Last Name']] else 'NULL'
            meet = row[headers['Meet']]
            date = row[headers['Meet Date']]
            event = row[headers['Event']]
            season = row[headers['Season']]
            relay = row[headers['Athletes']] if row[headers['Athletes']] else 'NULL'
            mark = row[headers['Mark']] if row[headers['Mark']] else 'NULL'
            school = row[headers['School']]
            category = row[headers['Category']]
            points = row[headers['Points']] if row[headers['Points']] else 'NULL'
            
            # Add school/athlete/season/event to relevant dictionary if new

            if meet != 'NULL':
                meet_key = f'{meet}+{season}'
                if meet_key not in meets:
                    meets[meet_key] = {'id': len(meets),
                                      'meet_name': meet,
                                      'meet_date': date}
                    
                else:
                    day = date[4:6]
                    month = date[:3]
                    meet_day = meets[meet_key]['meet_date'][4:6]
                    meet_month = meets[meet_key]['meet_date'][:3]
                    if day < meet_day or (month != meet_month and day > meet_day):
                        meets[meet_key]['meet_date'] = date

            if school != 'NULL':
                school_key = f'{school}'
                if school_key not in schools:
                    schools[school_key] = {'id': len(schools),
                                           'school_name': school}
            
            
            
            if first_name != 'NULL':
                athlete_key = f'{first_name}+{last_name}+{school}'
                if athlete_key not in athletes:
                    athletes[athlete_key] = {'id': len(athletes),
                                             'school_year': schoolYear,
                                             'first_name': first_name,
                                             'last_name': last_name,
                                             'school': school,
                                             'gender': category}
                    
            if season != 'NULL':
                season_key = f'{season}'
                if season_key not in seasons:
                    
                    seasons[season_key] = {"id": len(seasons),
                                          "season_name": season,
                                          'season_category': 0 if season.split()[0] == 'Indoor' else 1}
                    
                    
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
                                     'season_category': 0 if season.split()[0] == 'Indoor' else 1}
                
            # Generate performance key to avoid potential duplicates

            if time != 'NULL':
                if relay == 'NULL':
                    performance_key = f'{first_name}+{last_name}+{school}+{event}+{date}+{time}'
                else:
                    performance_key = f'{relay}+{event}+{school}+{date}+{time}'
                result = parse_time(time)
            elif points != 'NULL':
                performance_key = f'{first_name}+{last_name}+{school}+{event}+{date}+{points}'
                result = int(points)
            else:
                performance_key = f'{first_name}+{last_name}+{school}+{event}+{date}+{mark}+{wind}'
                result = float(mark[:-1])

            if performance_key not in performances:

                performances[performance_key] = {'id': len(performances),
                                                 'mark': result,
                                                 'wind': wind,
                                                 'result_date': date,
                                                 'meet': meet}
                
            # Add performance to results, linked to correct school/athlete etc. also handling relays
            if relay == 'NULL':
                results.append((athletes[athlete_key]['id'],performances[performance_key]['id'],schools[school_key]['id'],events[event_key]['id'],seasons[season_key]['id'],meets[meet_key]['id']))
            else:
                relay_team = relay.split(',')
                for leg in relay_team:
                    for athlete_key in athletes:
                        if athletes[athlete_key]['last_name'] == leg and athletes[athlete_key]['school'] == school:
                            results.append((athletes[athlete_key]['id'],performances[performance_key]['id'],schools[school_key]['id'],events[event_key]['id'],seasons[season_key]['id'],meets[meet_key]['id']))

    # Write resulting dictionaries/lists to csv files

    with open('meets.csv', 'w') as f:
        writer = csv.writer(f)
        for meet_key in meets:
            meet = meets[meet_key]
            row = (meet['id'], meet['meet_name'], meet['meet_date'])
            writer.writerow(row)

    with open('schools.csv', 'w') as f:
        writer = csv.writer(f)
        for school_key in schools:
            school = schools[school_key]
            row = (school['id'], school['school_name'])
            writer.writerow(row)

    with open('seasons.csv', 'w') as f:
        writer = csv.writer(f)
        for season_key in seasons:
            season = seasons[season_key]
            row = (season['id'], season['season_name'], season['season_category'])
            writer.writerow(row)
            
    with open('athletes.csv', 'w') as f:
        writer = csv.writer(f)
        for athlete_key in athletes:
            athlete = athletes[athlete_key]
            row = (athlete['id'], athlete['last_name'], athlete['first_name'], athlete['gender'])
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
            row = (performance['id'], performance['mark'], performance['wind'], performance['result_date'])
            writer.writerow(row)

    with open('results.csv', 'w') as f:
        writer = csv.writer(f)
        for athlete_id, performance_id, school_id, event_id, season_id, meet_id in results:
            writer.writerow((athlete_id, performance_id, school_id, event_id, season_id, meet_id))
                    
if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} original_csv_file', file=sys.stderr)
    exit()

main(sys.argv[1])