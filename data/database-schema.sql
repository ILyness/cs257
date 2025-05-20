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
    season_name text,
    season_category integer NOT NULL --- do we want to include this? so its easy to filter to look through all indoor seasons or all outdoor seasons?
)

CREATE TABLE meets (
    id integer NOT NULL,
    meet_name text,
    meet_date date
)

CREATE TABLE events ( -- this table will likely be used often for population of dropdowns/populating returned tables with event names 
    id integer NOT NULL,
    event_name text,
    event_category text, --indoor vs outdoor? or track vs field?
    season_category integer NOT NULL -- indoor vs outdoor ids, indoor = 0, outdoor = 1. it's important when we look at times to know whether that time was run indoor or outdoor
);

CREATE TABLE performances (
    id integer NOT NULL, 
    mark float,
    wind float,
    result_date date
);

CREATE TABLE results (  -- keeping this table, as multiple athletes can refer to a single performance (relays)
    athlete_id integer, --REFERS TO table athletes table id
    performance_id integer, -- REFERS TO performances table id 
    school_id integer, -- REFERS TO schools table id
    event_id integer, -- REFERS TO event table id
    season_id integer, -- REFERS TO seasons table id
    meet_id integer
);
