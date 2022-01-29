DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS vacuum_settings;
DROP TABLE IF EXISTS mop_settings;
DROP TABLE IF EXISTS cleaning_schedule;
DROP TABLE IF EXISTS cleaning_history;
DROP TABLE IF EXISTS resource_level;
DROP TABLE IF EXISTS battery_level;
DROP TABLE IF EXISTS bin_level;
DROP TABLE IF EXISTS air_quality;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE cleaning (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  type BINARY NOT NULL, -- 0 for vacuuming, 1 for mopping
  settings_v INTEGER NOT NULL,
  settings_m INTEGER NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (settings_v) REFERENCES vacuum_settings(id),
  FOREIGN KEY (settings_m) REFERENCES mop_settings(id)
);

-- vacuum settings
CREATE TABLE vacuum_settings (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  frequency INTEGER NOT NULL, -- 1 pass, 2 pass etc
  power REAL NOT NULL
);

-- mop settings
CREATE TABLE mop_settings (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  frequency INTEGER NOT NULL
);

-- cleaning schedule
CREATE TABLE cleaning_schedule (
  type BINARY NOT NULL, -- 0 for vacuuming, 1 for mopping
  date TIMESTAMP NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (type) REFERENCES cleaning(type),
  PRIMARY KEY (type, date)
);

-- cleaning history
CREATE TABLE cleaning_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  elapsed_time REAL NOT NULL,
  type BINARY NOT NULL, -- 0 for vacuuming, 1 for mopping
  date TIMESTAMP NOT NULL,
  FOREIGN KEY (type) REFERENCES cleaning(type)
);

-- detect level of cleaning products
CREATE TABLE resource_level (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  value REAL NOT NULL
);

-- battery level
CREATE TABLE battery_level (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  value REAL NOT NULL
);

-- bin full level
CREATE TABLE bin_level (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  value REAL NOT NULL
);

-- air quality data
CREATE TABLE air_quality (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value REAL NOT NULL
);