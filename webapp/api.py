import sys
import psycopg2
import config
import json
import flask
import argparse

app = flask.Flask(__name__)

def get_connection():
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/list')
def get_performance_list():
    events = []
    performance_list = {}
    limit = flask.request.args.get('num_entries', type=int, default=20)
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = 'SELECT * FROM events'
        cursor.execute(query)

        for row in cursor:
            events.append({'id':row[0], 'event_name':row[1], 'event_category':row[2], 'season_category':row[3]})

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()

    for event in events:
        if event['season_category'] == 0:
            continue
        params = (event['id'],)
        performance_list[event['event_name']] = []
        query = 'SELECT athletes.first_name || \' \' || athletes.last_name AS athlete_name, schools.school_name, performances.mark, performances.result_date, performances.meet ' \
                'FROM events ' \
                'JOIN results ON events.id=results.event_id ' \
                'JOIN athletes ON athletes.id=results.athlete_id ' \
                'JOIN performances ON performances.id=results.performance_id ' \
                'JOIN schools on schools.id=results.school_id ' \
                'JOIN seasons on seasons.id=results.season_id ' \
                'WHERE events.id=%s ' \
                'AND seasons.season_name=\'Outdoor 2025\' '
        
        if event['event_category'] == 'Running':
            query += f'ORDER BY performances.mark;'
        else:
            query += f'ORDER BY performances.mark DESC;'

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            athletes = set()
            i = 1
            for row in cursor:
                if i > limit:
                    break
                if row[0] in athletes:
                    continue
                athletes.add(row[0])
                i += 1
                performance_list[event['event_name']].append({'athlete_name':row[0] if 'Relay' not in event['event_name'] else 'NULL', 'school':row[1], 'mark':row[2], 'date':str(row[3]), 'meet':row[4]})

        except Exception as e:
            print(e, file=sys.stderr)

        connection.close()
    return json.dumps(performance_list, indent=4)

@app.route('/athlete/<id>')
def get_athlete(id):
    ''' Returns '''
    athlete = []
    params = [id, id]
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()
        # Execute the query
        query = '''SELECT athletes.first_name, athletes.last_name, athletes.gender, schools.school_name, events.event_name, events.event_category, performances
                    FROM athletes
                    JOIN results ON results.athlete_id= %s
                    JOIN schools ON results.school_id = schools.id
                    JOIN performances ON results.performance_id = performances.id
                    JOIN events ON results.event_id = events.id
                    WHERE athletes.id= %s
                    GROUP BY athletes.first_name, athletes.last_name, athletes.gender, schools.school_name, events.event_name, events.event_category, performances'''
        
        cursor.execute(query, params)

        for row in cursor:
            athlete.append(f'{row[0], row[1], row[2], row[3]}')
            marks = []
            athlete.append(marks)
            break
        for row in cursor:
            marks.append(f'{row[4],row[5],row[6],}')
            


    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return json.dumps(athlete)

@app.route('/athletes')
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

@app.route('/marks/<gender>/<event>')
def get_marks(gender,event):
    marks = []
    try:
        mark = flask.request.args.get('mark', type=float)
        school = flask.request.args.get('school')
        season = flask.request.args.get('season')
        duplicate = flask.request.args.get('duplicate')
        display_number = flask.request.args.get('display_number', default=20,type=int)
        if duplicate: #havent added functionality for this
            if duplicate == "True":
                duplicate = True
            else:
                duplicate = False
        query = '''SELECT CONCAT(athletes.first_name + " " + athletes.last_name) as athlete_name, events.event_name, seasons.season_name, performances.mark, performances.result_date
                        FROM results 
                        JOIN performances ON performances.id = results.performance_id
                        JOIN events ON results.event_id = events.id 
                        AND events.event_name = %s
                        JOIN athletes ON athletes.id = results.athletes_id AND athletes.gender = %s
                        JOIN seasons ON results.season_id = seasons.id
                        JOIN schools ON schools.id = results.school_id'''
        parameters = [event,gender]
        
        if season:
            query = query + ''' WHERE seasons.season_name = %s'''
            parameters.append[season]
            
        if school:
            query = query + ''' AND school_name = %s'''
            parameters.append[school]
            
        if display_number:
            query = query + '''LIMIT %s'''
            parameters.append[display_number]
            
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        for row in cursor:
            marks.append({'athlete_name': row[0], 'event_name': row[1], 'season_name': row[2], 'mark': row[3], 'result_date': row[4]})
    
    
        query2 = '''SELECT event_category FROM events WHERE event_name = %s'''
        cursor.execute(query2, (event,))
        for row in cursor:
            event_category = row[0]
        connection.close() 
        
        if event_category == "Running":
            marks = sorted(marks, key = lambda x: parse_time(x['mark']))
        elif event_category == "Multi":
            marks = sorted(marks, key = lambda x: float(x['mark'][:-1]), reverse = True)
        elif event_category == "Field":    
            marks = sorted(marks, key = lambda x: float(x['mark']), reverse = True)
                
        if mark: #filters results by mark
            if event_category == "Running":
                for result in marks[:]:
                    if parse_time(result['mark']) > parse_time(mark):
                        marks.remove(result)
            elif event_category == "Multi":
                for result in marks[:]:
                    if float(result['mark']) < float(mark):
                        marks.remove(result)
            elif event_category == "Field":  
                for result in marks[:]:
                    if float(result['mark'][:-1]) < float(mark[:-1]):
                        marks.remove(result)
                            
        if not duplicate: ## not sure if there is an easier way to remove duplicates from the list of dictionaries
            seen = set()
            to_delete = []
            for i in range(len(marks)):
                name = (marks[i]['first'], marks[i]['last'])
                if name in seen:
                    to_delete.append(i)
                else:
                    seen.add(name)
            
            for i in reversed(to_delete):
                del marks[i]
        
        
    except Exception as e:
        print(e, file=sys.stderr)
    
    return json.dumps(marks)



@app.route('/help')
def get_help():
    return flask.render_template('help.html')


def parse_time(t):  
    if ':' in t:
        minutes, seconds = t.split(':')
        return int(minutes) * 60 + float(seconds)
    else:
        
        return float(t)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Flask API implementation using SQL database via psycopg2')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
