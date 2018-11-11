-- SQLite - Working Correctly...

-- Foreign key support is not enabled in SQLite by default.
-- It needs to be enable manually each for each connection using the following pragma...
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;
/*
If foreign key constraints are enabled, a DROP TABLE command performs an implicit DELETE FROM command before 
removing the table from the database schema. Any triggers attached to the table are dropped from the database 
schema before the implicit DELETE FROM is executed, so this cannot cause any triggers to fire
*/
DROP TABLE IF EXISTS Outcomes;
DROP TABLE IF EXISTS Battles;
DROP TABLE IF EXISTS Ships;
DROP TABLE IF EXISTS Classes;


CREATE TABLE Classes (
    className    VARCHAR2(20),
    typeClass    CHAR(2),
    country      VARCHAR2(15),
    numGuns      INT,
    bore         INT,
    displacement INT,
    CONSTRAINT pkClasses PRIMARY KEY (className),
    CHECK (typeClass IN ('bb', 'bc'))
);

CREATE TABLE Ships
  (
     shipName  VARCHAR2(20),
     shipClass VARCHAR2(20),
     launchYr  INT,
     CONSTRAINT pkShips PRIMARY KEY (shipName),
     CONSTRAINT fkClasses FOREIGN KEY (shipClass) REFERENCES Classes (className)
  );

CREATE TABLE Battles
  (
      battleName VARCHAR2(20),
      battleYr   INT,
      CONSTRAINT pkBattles PRIMARY KEY (battleName)
   );

CREATE TABLE Outcomes
  (
      ship    VARCHAR2(20),
      battle  VARCHAR2(20),
      outcome VARCHAR2(10),
      CONSTRAINT pkOutcomes PRIMARY KEY (ship, battle),
      CHECK (outcome IN ('sunk', 'ok', 'damaged')),
      CONSTRAINT fkShips FOREIGN KEY (ship) REFERENCES Ships (shipName),
      CONSTRAINT fkBattles FOREIGN KEY (battle) REFERENCES Battles (battleName)
  );

----------------------------
-- Views for App homework --
----------------------------
DROP VIEW vShipClass;
DROP VIEW vBattle;

CREATE VIEW vShipClass AS
SELECT c.country, s.shipName, s.launchYr, c.className, c.typeClass, c.numGuns, c.bore, c.displacement, (SELECT MIN(outcome) FROM Outcomes WHERE s.shipName = ship) AS condition
FROM Ships s
    , Classes c
WHERE s.shipClass = c.className
ORDER BY c.country;

CREATE VIEW vBattle AS
SELECT b.battleYr, b.battleName, o.ship AS shipName, o.outcome
FROM Outcomes o
    , Battles b
WHERE o.battle = b.battleName
ORDER BY b.battleYr;
----------------------------
    

INSERT INTO Classes VALUES ('Bismarck', 'bb', 'Germany', 8, 15, 42000);
INSERT INTO Classes VALUES ('Iowa', 'bb', 'USA', 9, 16, 46000);
INSERT INTO Classes VALUES ('Kongo', 'bc', 'Japan', 8, 14, 32000);
INSERT INTO Classes VALUES ('North Carolina', 'bb', 'USA', 9, 16, 37000);
INSERT INTO Classes VALUES ('Renown', 'bc', 'Gt. Britain', 6, 15, 32000);
INSERT INTO Classes VALUES ('Revenge', 'bb', 'Gt. Britain', 8, 15, 29000);
INSERT INTO Classes VALUES ('Tennessee', 'bb', 'USA', 12, 14, 32000);
INSERT INTO Classes VALUES ('Yamato', 'bb', 'Japan', 9, 18, 65000);

INSERT INTO Battles VALUES ('Denmark Strait', 1941);
INSERT INTO Battles VALUES ('Guadalcanal', 1942);
INSERT INTO Battles VALUES ('North Cape', 1943);
INSERT INTO Battles VALUES ('Surigao Strait', 1944);

INSERT INTO Ships VALUES ('California', 'Tennessee', 1921);
INSERT INTO Ships VALUES ('Haruna', 'Kongo', 1915);
INSERT INTO Ships VALUES ('Hiei', 'Kongo', 1914);
INSERT INTO Ships VALUES ('Iowa', 'Iowa', 1943);
INSERT INTO Ships VALUES ('Kirishima', 'Kongo', 1915);
INSERT INTO Ships VALUES ('Kongo', 'Kongo', 1913);
INSERT INTO Ships VALUES ('Missouri', 'Iowa', 1944);
INSERT INTO Ships VALUES ('Musashi', 'Yamato', 1942);
INSERT INTO Ships VALUES ('New Jersey', 'Iowa', 1943);
INSERT INTO Ships VALUES ('North Carolina', 'North Carolina', 1941);
INSERT INTO Ships VALUES ('Ramillies', 'Revenge', 1917);
INSERT INTO Ships VALUES ('Renown', 'Renown', 1916);
INSERT INTO Ships VALUES ('Repulse', 'Renown', 1916);
INSERT INTO Ships VALUES ('Resolution', 'Revenge', 1916);
INSERT INTO Ships VALUES ('Revenge', 'Revenge', 1916);
INSERT INTO Ships VALUES ('Royal Oak', 'Revenge', 1916);
INSERT INTO Ships VALUES ('Royal Sovereign', 'Revenge', 1916);
INSERT INTO Ships VALUES ('Tennessee', 'Tennessee', 1920);
INSERT INTO Ships VALUES ('Washington', 'North Carolina', 1941);
INSERT INTO Ships VALUES ('Wisconsin', 'Iowa', 1944);
INSERT INTO Ships VALUES ('Yamato', 'Yamato', 1941);

INSERT INTO Outcomes VALUES ('California', 'Surigao Strait', 'ok');
INSERT INTO Outcomes VALUES ('Kirishima', 'Guadalcanal', 'sunk');
INSERT INTO Outcomes VALUES ('North Carolina', 'Guadalcanal', 'damaged');
INSERT INTO Outcomes VALUES ('Tennessee', 'Surigao Strait', 'ok');
INSERT INTO Outcomes VALUES ('Washington', 'Guadalcanal', 'ok');
INSERT INTO Outcomes VALUES ('North Carolina', 'Surigao Strait', 'ok');

END TRANSACTION; -- an alias for COMMIT.


