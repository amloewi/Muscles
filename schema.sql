CREATE TABLE person (
	name TEXT PRIMARY KEY,
	email TEXT
);

CREATE TABLE workout (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	person_id TEXT,
	date DATETIME --"YYYY-MM-DD HH:MM:SS"
);

CREATE TABLE exercise (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	workout_id INTEGER,
	muscle TEXT,
	sets INTEGER,  -- SOMETIMES, (often?) these will be empty --- default 0?
	reps INTEGER,
	weight INTEGER
);

CREATE TABLE person_workout (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	workout_id INTEGER,
	date DATETIME -- this saves one call, but it was being strange
);

CREATE TABLE workout_exercise (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	workout_id INTEGER,
	exercise_id INTEGER
);

-- if every ... exercise just has a name and a date, then there could be multiple people with the same name. no good! BUT--- if there's a separate name database that just has ... whatsit --- the names --- that can be kept from happening. HOWEVER: if I want all of the ... exercises from the most recent workout, for example, for a particular person (which is what I want, of course, and at a base the ONLY thing that I want: ) what is easiest? if I have exercise ... ids, then I can just (but I don't know HOW to make exercise ids. So ... try it out on fuck.)