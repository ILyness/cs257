CREATE TABLE athletes (
    id integer NOT NULL,
    last_name text,
    first_name text,
    gender text
);

CREATE TABLE schools (
    id integer NOT NULL,
    school_name text
)

CREATE TABLE seasons (
    id integer NOT NULL,
    season_name text
)

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
);

CREATE TABLE results (  -- keeping this table, as multiple athletes can refer to a single performance (relays)
    athlete_id integer, --REFERS TO table athletes id
    performance_id integer, -- REFERS TO performances id 
    school_id integer,
    event_id integer,
    season_id integer
);
