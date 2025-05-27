''' api.py
    Api implementation using flask and SQL via psycopg2.
    Daniel, Soren, Indy
    Insprired/modeled from Jeff Ondich's sample(s)'''

import sys
import psycopg2
import config
import json
import flask
import argparse

api = flask.Blueprint('api', __name__)

def display_mark(mark, event_category):
    if event_category == 'Running':
        minutes = float(mark) // 60
        seconds = float(mark) % 60
        if minutes == 0:
            return f'{seconds:05.2f}'
        else:
            return f'{minutes:.0f}:{seconds:05.2f}'
    elif event_category == 'Field':
        return f'{float(mark):.2f}m'
    else:
        return f'{mark}'

def get_connection():
    """Get connection to SQL database, and throw error if there is a problem"""
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@api.route('/seasons/')
def get_seasons():
    """Endpoint to return list of all seasons to populate dropdown."""
    seasons = []
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """SELECT * FROM seasons"""
        cursor.execute(query)
        for row in cursor:
            seasons.append({'season_name':row[1], 'season_category':row[2]})
        connection.close()
        return json.dumps(seasons)
    
    except Exception as e:
        print(e, file=sys.stderr)

@api.route('/list/')
def get_performance_list():
    """Endpoint to get the top specified number of performances from each event. Not very flexible but puts lots of
    useful information in the same place."""
    events = []
    performance_list = {}
    season = flask.request.args.get('season', type=str, default='Outdoor 2025')
    limit = flask.request.args.get('num_entries', type=int, default=20)
    params = (season,)
    # Connect to database and grab all events
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """SELECT * FROM events
                JOIN seasons ON seasons.season_category = events.season_category
                WHERE seasons.season_name LIKE %s;"""
        cursor.execute(query, params)

        for row in cursor:
            events.append({'id':row[0], 'event_name':row[1], 'event_category':row[2], 'season_category':row[3]})


        # Go through each event that matches the current season, and grab the top performances from each one. Season is currently hardcoded
        # to Outdoor 2025 but ultimtaley multiple seasons will be available.
        for event in events:
            params = (event['id'],season)
            performance_list[event['event_name']] = []
            # Build query for current event
            query2 = """SELECT athletes.first_name || \' \' || athletes.last_name AS athlete_name, schools.school_name, performances.mark, performances.result_date, meets.meet_name
                    FROM events
                    JOIN results ON events.id=results.event_id
                    JOIN athletes ON athletes.id=results.athlete_id
                    JOIN performances ON performances.id=results.performance_id
                    JOIN schools on schools.id=results.school_id
                    JOIN seasons on seasons.id=results.season_id
                    JOIN meets on meets.id=results.meet_id
                    WHERE events.id=%s
                    AND seasons.season_name LIKE %s """
            
            if event['event_category'] == 'Running':
                query2 += f'ORDER BY performances.mark;'
            else:
                query2 += f'ORDER BY performances.mark DESC;'

            cursor.execute(query2, params)
            unique_performers = set()
            i = 1
            if 'Relay' in event['event_name']:
                criteria = 1
            else:
                criteria = 0
            for row in cursor:
                if i > limit:
                    break
                if row[criteria] in unique_performers:
                    continue
                unique_performers.add(row[criteria])
                i += 1
                performance_list[event['event_name']].append({'athlete_name':row[0] if 'Relay' not in event['event_name'] else 'NULL', 
                                                            'school':row[1], 'mark':display_mark(row[2],event['event_category']), 
                                                            'date':str(row[3]), 
                                                            'meet':row[4]})
        connection.close()
        return json.dumps(performance_list)

    except Exception as e:
        print(e, file=sys.stderr)


@api.route('/athlete/<id>')
def get_athlete(id):
    ''' Returns '''
    athlete = {}
    params = [id, id]
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()
        # Execute the query
        query = '''SELECT athletes.first_name, athletes.last_name, athletes.gender, schools.school_name, events.event_name, events.event_category, meets.meet_name, performances
                    FROM athletes
                    JOIN results ON results.athlete_id= %s
                    JOIN schools ON results.school_id = schools.id
                    JOIN performances ON results.performance_id = performances.id
                    JOIN events ON results.event_id = events.id
                    JOIN meets ON results.meet_id = meets.id
                    WHERE athletes.id= %s
                    GROUP BY athletes.first_name, athletes.last_name, athletes.gender, schools.school_name, events.event_name, events.event_category, meets.meet_name, performances'''
        
        cursor.execute(query, params)

        for row in cursor:
            athlete = {'first_name':row[0], 'last_name':row[1], 'gender':row[2], 'school':row[3], 'marks': {}}
            break
        for row in cursor:
            if row[4] not in athlete['marks']:
                athlete['marks'][row[4]] = []
            fields = row[7].split(',')
            athlete['marks'][row[4]].append({'mark':display_mark(fields[1], event_category=row[5]), 'meet':row[6], 'date':fields[3]})
            


    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return json.dumps(athlete)

@api.route('/athletes')
def get_athletes():
    ''' Returns a list of all the athletes in the database, with eiter a first or last name matching with the search_string". '''
    search_string = flask.request.args.get('search', '')
    athletes = []
    params = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        if ' ' in search_string:
            strings = search_string.split(' ')
            search_string1 = strings[0]
            search_string2 = strings[1]
            params.extend([search_string1, search_string1, search_string2, search_string2])
            query = '''SELECT athletes.first_name, athletes.last_name, athletes.gender, schools.school_name 
                        FROM athletes 
                        JOIN results ON athletes.id = results.athlete_id
                        JOIN schools ON schools.id = results.school_id
                        WHERE (athletes.first_name ILIKE %s
                        OR athletes.last_name ILIKE %s) 
                        AND (athletes.last_name ILIKE %s
                        OR athletes.first_name ILIKE %s)
                        GROUP BY athletes.first_name, athletes.last_name, athletes.gender, schools.school_name
                        ORDER BY athletes.first_name, athletes.last_name, schools.school_name'''
        else:
            search_string = f'%{search_string}%'
            params.extend([search_string, search_string])
            query = '''SELECT athletes.first_name, athletes.last_name, athletes.gender, schools.school_name 
                        FROM athletes 
                        JOIN results ON athletes.id = results.athlete_id
                        JOIN schools ON schools.id = results.school_id
                        WHERE athletes.first_name ILIKE %s OR athletes.last_name ILIKE %s
                        GROUP BY athletes.first_name, athletes.last_name, athletes.gender, schools.school_name
                        ORDER BY athletes.first_name, athletes.last_name, schools.school_name'''

        cursor.execute(query, params)
        # Iterate over the query results to produce the list of athletes, their school, and their gender.
        for row in cursor:
            athletes.append({
                'first_name': row[0],
                'last_name': row[1],
                'school': row[3],
                'gender': row[2]
            })


    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return json.dumps({'athletes': athletes})

@api.route('/search')
def get_marks():
    
    marks = []
    try:
        event = flask.request.args.get('event', type=str)
        gender = flask.request.args.get('gender', type=bool)
        duplicates = flask.request.args.get('duplicates', type=bool)
        team = flask.request.args.get('team')
        season = flask.request.args.get('season')
        meet = flask.request.args.get('meet')
        mark = flask.request.args.get('mark', type=str)
        
        
        
        display_number = flask.request.args.get('display_number', default=20,type=int)

        connection = get_connection()
        cursor = connection.cursor()

        query2 = '''SELECT event_category FROM events WHERE event_name = %s'''
        cursor.execute(query2, (event,))
        for row in cursor:
            event_category = row[0]
    
        query = '''SELECT CONCAT(athletes.first_name, athletes.last_name) as athlete_name, events.event_name, seasons.season_name, performances.mark, performances.result_date
                        FROM results 
                        JOIN performances ON performances.id = results.performance_id
                        JOIN events ON results.event_id = events.id 
                        AND events.event_name = %s
                        JOIN athletes ON athletes.id = results.athlete_id AND athletes.gender = %s
                        JOIN seasons ON results.season_id = seasons.id
                        JOIN schools ON schools.id = results.school_id'''
        
                       # JOIN meets ON meets.id = results.meet_id
        parameters = [event,gender]
        
        if season:
            query = query + ''' WHERE seasons.season_name = %s'''
            parameters.append(season)
            
        if team:
            query = query + ''' AND school_name = %s'''
            parameters.append(team)

        if meet:
            query = query + ''' AND meet_name = %s'''
            parameters.append(team)
            
       
        cursor.execute(query, parameters)
        for row in cursor:
            marks.append({'athlete_name': row[0], 'event_name': row[1], 'team': row[2], 'season_name': row[3], 'mark': display_mark(row[4],event_category=event_category), 'meet' : row[5], 'result_date': row[6].isoformat(), 'num_marks':None})
    
        connection.close() 
        
        if event_category == "Running":
            marks = sorted(marks, key = lambda x: x['mark'])
        elif event_category == "Multi":
            marks = sorted(marks, key = lambda x: x['mark'], reverse = True)
        elif event_category == "Field":    
            marks = sorted(marks, key = lambda x: x['mark'], reverse = True)
            
            
        
        
                
        if mark: #filters results by mark
            filtered_marks = []
            if event_category == "Running":
                for result in marks[:]:
                    if parse_time(result['mark']) <= parse_time(mark):
                        filtered_marks.append(result)
            elif event_category == "Multi":
                for result in marks[:]:
                    if float(result['mark']) >= float(mark):
                        filtered_marks.append(result)
            elif event_category == "Field":  
                for result in marks[:]:
                    if float(result['mark'][:-1]) >= float(mark[:-1]):
                        filtered_marks.append(result)
            marks = filtered_marks
            del(filtered_marks)
            
            
        if duplicates == "False": ## not sure why, but when I had this if statement AFTER the mark check, duplicates athletes would be allowed through if mark was included as a variable
            seen = {}
            to_delete = []
            for i in range(len(marks)):
                name = (marks[i]['athlete_name'])
                if name in seen:
                    to_delete.append(i)
                    if mark:
                        marks[seen.get(name)]['num_marks'] += 1 
                else:
                    seen[name] = i
                    if mark:
                        marks[i]['num_marks'] = 1
            
            for i in reversed(to_delete):
                del marks[i]
        
       
        if display_number:
              marks = marks[:display_number]   
    except Exception as e:
        print(e, file=sys.stderr)
    print("running marks")
    return json.dumps(marks)





@api.route('/help')
def get_help():
    return flask.render_template('help.html')


#used for sorting and filtering with running events, as the mark is MM:SS.SS
def parse_time(t):  
    if ':' in t:
        minutes, seconds = t.split(':')
        return int(minutes) * 60 + float(seconds)
    else:
        
        return float(t)

'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Flask API implementation using SQL database via psycopg2')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    api.run(host=arguments.host, port=arguments.port, debug=True)
'''