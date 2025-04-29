CREATE TABLE athletes (
    id integer NOT NULL,
    last_name text,
    first_name text,
    school text,
    gender text
);

CREATE TABLE events (
    id integer NOT NULL,
    event_name text,
    event_category text
);

CREATE TABLE performances (
    id integer NOT NULL,
    mark text,
    wind text,
    result_date text,
    meet text,
    season text
);

CREATE TABLE athletes_performances (
    athlete_id integer,
    performance_id integer
);

CREATE TABLE events_performances (
    event_id integer,
    performance_id integer
);