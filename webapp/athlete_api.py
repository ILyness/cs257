'''adapted from sample from jeff
ILIKE and tuple paramter with %s from internet'''
import sys
import psycopg2
import config
import flask
import json

app = flask.Flask(__name__)

def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/athlete_page/<id>')
def get_athlete(id):
    ''' Returns '''
    athlete = []
    id = f'{id}'
    params = [id, id]
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()
        # Execute the query
        query = '''SELECT athletes.first_name, athletes.last_name, athletes.gender, schools.school_name, events.event_name, events.event_category, performances
                    FROM athletes
                    JOIN results ON results.athlete_id ILIKE %s
                    JOIN schools ON results.school_id = schools.id
                    JOIN performances ON results.performance_id = performances.id
                    JOIN events ON results.event_id = events.id
                    WHERE athletes.id ILIKE %s
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

app.run('localhost', config.port, debug=True)
