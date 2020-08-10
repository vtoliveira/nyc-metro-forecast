\copy mta FROM PROGRAM 'gzip -dc 2010.csv.gz' DELIMITER ',' CSV HEADER NULL '';
\copy mta FROM PROGRAM 'gzip -dc 2011.csv.gz' DELIMITER ',' CSV HEADER NULL '';
\copy mta FROM PROGRAM 'gzip -dc 2012.csv.gz' DELIMITER ',' CSV HEADER NULL '';
\copy mta FROM PROGRAM 'gzip -dc 2013.csv.gz' DELIMITER ',' CSV HEADER NULL '';
\copy mta FROM PROGRAM 'gzip -dc 2014.csv.gz' DELIMITER ',' CSV HEADER NULL '';
\copy mta FROM PROGRAM 'gzip -dc 2015.csv.gz' DELIMITER ',' CSV HEADER NULL '';
\copy mta FROM PROGRAM 'gzip -dc 2016.csv.gz' DELIMITER ',' CSV HEADER NULL '';
\copy mta FROM PROGRAM 'gzip -dc 2017.csv.gz' DELIMITER ',' CSV HEADER NULL '';

ALTER TABLE mta ALTER exits TYPE numeric USING exits::float8;
ALTER TABLE mta ALTER entries TYPE numeric USING entries::float8;

ALTER TABLE mta ADD COLUMN turnstile text;
UPDATE mta SET turnstile = ca || '-' || unit || '-' || scp;
