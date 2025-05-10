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
    
    if event_category = "Running":
        marks = sorted(marks, key = lambda x: parse_time(x['mark']))
    else if event_category = "Multi":
        marks = sorted(marks, key = lambda x: float(x['mark'][:-1]), reverse = True)
    else if event_category = "Field":    
        marks = sorted(marks, key = lambda x: float(x['mark']), reverse = True)
            
    if mark: #filters results by mark
        if event_category = "Running":
            for result in marks[:]:
                if parse_time(result['mark']) > parse_time(mark):
                    marks.remove(result)
        else if event_category = "Multi":
            for result in marks[:]:
                if float(result['mark']) < float(mark):
                    marks.remove(result)
        else if event_category = "Field":  
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
        
        
    excecpt Exception as e:
        print(e, file=sys.stderr)
    
    return marks









################################################################
@app.route('/help')
def get_help():
    return flask.render_template('help.html')



def parse_time(t):  
    if ':' in t:
        minutes, seconds = t.split(':')
        return int(minutes) * 60 + float(seconds)
    else:
        
        return float(t)



def main():
    print('========== 10 Marks ==========') ## for now it just should get the first 10 results. wanna make sure config and stuff works.
    marks = get_marks()
    for mark in marks:
        print(f"{mark['Result1']} {mark['Result2']}")
    print()
    
    
    
    
if __name__ == '__main__':
    app.run(host=config.host, port=config.port, debug=True)
    