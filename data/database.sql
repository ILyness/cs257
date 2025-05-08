CREATE TABLE athletes (
    id integer NOT NULL,
    last_name text,
    first_name text,
    gender text
);

\copy athletes FROM 'athletes.csv' DELIMITER ',' CSV NULL AS 'NULL';

CREATE TABLE schools (
    id integer NOT NULL,
    school_name text
);

\copy schools FROM 'schools.csv' DELIMITER ',' CSV NULL AS 'NULL';

CREATE TABLE seasons (
    id integer NOT NULL,
    season_name text,
    season_category --- do we want to include this? so its easy to filter to look through all indoor seasons or all outdoor seasons?
);

\copy seasons FROM 'seasons.csv' DELIMITER ',' CSV NULL AS 'NULL';


CREATE TABLE events ( -- this table will likely be used often for population of dropdowns/populating returned tables with event names 
    id integer NOT NULL,
    event_name text,
    event_category text, --indoor vs outdoor? or track vs field?
    season_category integer NOT NULL -- indoor vs outdoor ids, indoor = 0, outdoor = 1. it's important when we look at times to know whether that time was run indoor or outdoor
);

\copy events FROM 'events.csv' DELIMITER ',' CSV NULL AS 'NULL';

CREATE TABLE performances (
    id integer NOT NULL, 
    mark text,
    wind text,
    result_date DATE, -- swapped text to datetime, so its easier to sort by date
    meet text
);

\copy performances FROM 'performances.csv' DELIMITER ',' CSV NULL AS 'NULL';

CREATE TABLE results (  -- keeping this table, as multiple athletes can refer to a single performance (relays)
    athlete_id integer, --REFERS TO table athletes table id
    performance_id integer, -- REFERS TO performances table id 
    school_id integer, -- REFERS TO schools table id
    event_id integer, -- REFERS TO event table id
    season_id integer -- REFERS TO seasons table id
);


\copy results FROM 'results.csv' DELIMITER ',' CSV NULL AS 'NULL';



