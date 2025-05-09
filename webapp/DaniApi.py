import sys
import psycopg2
import argparse
import flask
import json
import csv
import config


def get_connection():
    try:
        return psycopg2.connect(database=config.database,
                                user = config.user,
                                password = config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/marks/<gender>/<event>')
def get_marks(gender,event):
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
        query = '''SELECT events.event_name FROM results 
                        JOIN performances ON performances.id = results.performance_id
                        JOIN events ON results.event_id = events.id 
                        AND events.event_name = %s
                        JOIN athletes ON athletes.gender = %s '''
        parameters = [event,gender]
        if season:
            query = query + ''' JOIN seasons 
                                ON results.season_id = seasons.id 
                                AND seasons.season_name = %s
                                        '''
            parameters.append[season]
        if school:
            query = query + ''' JOIN schools
                                ON schools.id = results.school_id
                                AND school_name = %s
                                        '''
            parameters.append[school]
            
        if mark: # less confident about this one, as it may need to be last cuz im filtering by stuff etc + only a basic functionalitiy for track events.
            query = query + "WHERE CAST(performances.mark AS FLOAT) < %s"
            parameters.append[mark]
        
        
        marks: []
    excecpt Exception as e:
        print(e, file=sys.stderr)
    
    return marks

@app.route('/help')
def get_help():
    return flask.render_template('help.html')


def main():
    print('========== 10 Marks ==========') ## for now it just should get the first 10 results. wanna make sure config and stuff works.
    marks = get_marks()
    for mark in marks:
        print(f"{mark['Result1']} {mark['Result2']}")
    print()
    
    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API for JEFFRS')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)