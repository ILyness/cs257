CREATE TABLE athletes (
    id integer NOT NULL,
    last_name text,
    first_name text,
    school text, -- this will have to be referenced in a dropdown for all schools in MIAC -- do we want to have a seperate table for schools? and have this be school ID? If we were doing more than MIACS it would be beneficial
    gender text
);

CREATE TABLE events ( -- this table will likely be used often for population of dropdowns/populating returned tables with event names 
    id integer NOT NULL,
    event_name text,
    event_category text, --indoor vs outdoor? or track vs field?
    season_category integer NOT NULL -- indoor vs outdoor ids, indoor = 0, outdoor = 1. it's important when we look at times to know whether that time was run indoor or outdoor
);

CREATE TABLE performances (
    id integer NOT NULL, 
    mark text,
    wind text,
    result_date DATE, -- swapped text to datetime, so its easier to sort by date
    meet text, 
    event_id, integer NOT NULL -- I changed season to event_id as it is possible for us to, with a given event id, determine whether this was run indoor or outdoor by querying events
);

CREATE TABLE athletes_performances ( 
    athlete_id integer, --REFERS TO table athletes id
    performance_id integer -- REFERS TO performances id 
);

CREATE TABLE events_performances ( -- including the ability to check for season category would allow us to pull all indoor 200m from 2020
    event_id integer,  --REFERS TO table events id
    performance_id integer  -- REFERS TO table performances id
);