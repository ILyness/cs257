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
    season text, --season this performance is from
    event_id, integer NOT NULL, -- REFERS TO table:events id

);

CREATE TABLE athletes_performances (  -- keeping this table, as multiple athletes can refer to a single performance (relays)
    athlete_id integer, --REFERS TO table athletes id
    performance_id integer -- REFERS TO performances id 
);
