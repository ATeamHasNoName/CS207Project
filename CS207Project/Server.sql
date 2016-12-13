CREATE TYPE level AS ENUM ('A', 'B', 'C', 'D', 'E', 'F');
CREATE TABLE timeseries (
    id integer PRIMARY KEY,
    mean float(16) NOT NULL,
    std float(16) NOT NULL,
    blarg float(16) NOT NULL,
    level level NOT NULL 
);

INSERT INTO timeseries (id, mean, std, blarg, level) VALUES (1, 0.5, 0.2, 0.245, 'A');
INSERT INTO timeseries (id, mean, std, blarg, level) VALUES (2, 0.1, 0.1, 0.444, 'C');