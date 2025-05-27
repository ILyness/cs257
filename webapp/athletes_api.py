
import sys
import psycopg2
import config
import flask
import json

app = flask.Flask(__name__)

def get_connection():
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()


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

app.run('localhost', config.port, debug=True)

