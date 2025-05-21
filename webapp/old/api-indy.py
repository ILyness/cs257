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
        performance_list[event['event_name']] = []
        query = 'SELECT athletes.first_name || \' \' || athletes.last_name AS athlete_name, schools.school_name, performances.mark, performances.result_date, performances.meet ' \
                'FROM events ' \
                'JOIN results ON events.id=results.event_id ' \
                'JOIN athletes ON athletes.id=results.athlete_id ' \
                'JOIN performances ON performances.id=results.performance_id ' \
                'JOIN schools on schools.id=results.school_id ' \
                'JOIN seasons on seasons.id=results.season_id ' \
                f'WHERE events.id={event['id']} ' \
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




@app.route('/help')
def get_help():
    return flask.render_template('help.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Flask API implementation using SQL database via psycopg2')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
