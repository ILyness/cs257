CREATE TABLE athletes (
    id integer NOT NULL,
    last_name text,
    first_name text,
    gender text
);

CREATE TABLE schools (
    id integer NOT NULL,
    school_name text
);

CREATE TABLE athletes_schools (
    athlete_id integer,
    school_id integer
)

CREATE TABLE events (
    id integer NOT NULL,
    event_name text
);