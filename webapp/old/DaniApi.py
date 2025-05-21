import sys
import psycopg2
import argparse
import flask
import json
import csv
import config

app = flask.Flask(__name__)


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
        mark = flask.request.args.get('mark', type=str)
        school = flask.request.args.get('school')
        season = flask.request.args.get('season')
        duplicate = flask.request.args.get('duplicate')
        display_number = flask.request.args.get('display_number', default=20,type=int)
    
        query = '''SELECT CONCAT(athletes.first_name, athletes.last_name) as athlete_name, events.event_name, seasons.season_name, performances.mark, performances.result_date
                        FROM results 
                        JOIN performances ON performances.id = results.performance_id
                        JOIN events ON results.event_id = events.id 
                        AND events.event_name = %s
                        JOIN athletes ON athletes.id = results.athlete_id AND athletes.gender = %s
                        JOIN seasons ON results.season_id = seasons.id
                        JOIN schools ON schools.id = results.school_id'''
        parameters = [event,gender]
        
        if season:
            query = query + ''' WHERE seasons.season_name = %s'''
            parameters.append(season)
            
        if school:
            query = query + ''' AND school_name = %s'''
            parameters.append(school)
            
       
            
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        for row in cursor:
            marks.append({'athlete_name': row[0], 'event_name': row[1], 'season_name': row[2], 'mark': row[3], 'result_date': row[4].isoformat(), 'num_marks':None})
    
        
        query2 = '''SELECT event_category FROM events WHERE event_name = %s'''
        cursor.execute(query2, (event,))
        for row in cursor:
            event_category = row[0]
        connection.close() 
        
        if event_category == "Running":
            marks = sorted(marks, key = lambda x: parse_time(x['mark']))
        elif event_category == "Multi":
            marks = sorted(marks, key = lambda x: float(x['mark']), reverse = True)
        elif event_category == "Field":    
            marks = sorted(marks, key = lambda x: float(x['mark'][:-1]), reverse = True)
            
            
        
        
                
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
            
            
        if duplicate == "False": ## not sure why, but when I had this if statement AFTER the mark check, duplicate athletes would be allowed through if mark was included as a variable
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
    