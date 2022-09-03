DROP TABLE IF EXISTS db;
DROP TABLE IF EXISTS times;
DROP TABLE IF EXISTS history;

CREATE TABLE db (
    feedAmount INT(10),
    treatAmount INT(10),
    numberOfFeedTimes INT(10),
    timezoneRegion TEXT(30),
    timezoneCity TEXT(30)
);

CREATE TABLE times (
    feedSchedules time
);

CREATE TABLE history(
    date time,
    log TEXT(30)
);
