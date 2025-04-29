CREATE TABLE athletes (
    id integer NOT NULL,
    last_name text,
    first_name text,
    gender text
);

CREATE TABLE schools (
    id integer NOT NULL,
    school text
)

CREATE TABLE athletes_schools (
    athlete_id integer,
    school_id integer
)

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
);

CREATE TABLE meets (
    id integer NOT NULL,
    meet text
)

CREATE TABLE seasons (
    id integer NOT NULL,
    season text
)

CREATE TABLE meets_performances (
    meet_id integer,
    performance_id integer
)

CREATE TABLE seasons_performances (
    season_id integer,
    performance_id integer
)

CREATE TABLE athletes_performances (
    athlete_id integer,
    performance_id integer
);

CREATE TABLE events_performances (
    event_id integer,
    performance_id integer
);