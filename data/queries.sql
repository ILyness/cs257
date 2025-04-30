SELECT * FROM athletes WHERE first_name = 'Indy'; 
-- Gets all athletes with a certain name




SELECT mark FROM performances, athletes_performances, athletes WHERE performances.id = athletes_performances.performance_id AND athlete_id = '303';
 --- Gets all marks by athlete Daniel Scheider


SELECT performances.mark, events.event_name FROM performances, athletes_performances, athletes, events WHERE athletes_performances.athlete_id = athletes.id AND performances.id = athletes_performances.performance_id AND events.id = performances.event_id AND athletes.id = 303 AND events.id = 2;
-- This query returns all marks from a specific athlete (Daniel Scheider), and a specific event (Outdoor 400m), from any season (JOINS would be easier but idk how deep into SQL you want us going right now)