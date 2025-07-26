CREATE DATABASE IF NOT EXISTS `stakes` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `stakes`;


-- Tabla “maestra”
CREATE TABLE `map` (
  `magId`               INT            NOT NULL,
  `segment`             INT,
  `lineDirectionTypeId` INT,
  `stake`               VARCHAR(9),
  `type`                DOUBLE,
  `epc`                 VARCHAR(24),
  `tid`                 DOUBLE,
  `polar`               TINYINT,
  `hidenEnable`         TINYINT,
  `transverse`          DOUBLE,
  `longitudinal`        DOUBLE,
  `curvature`           DOUBLE,
  `coordinateX`         DOUBLE,
  `coordinateY`         DOUBLE,
  `coordinateE`         INT,
  `coordinateN`         INT,
  `cruisingSpeed`       INT,
  `limitSpeed`          INT,
  `scene`               TINYINT,
  `stationType`         DOUBLE,
  `stationNum`          INT,
  `signallamp`          TINYINT,
  `oneWayRoad`          TINYINT,
  `meetingVec`          TINYINT,
  `oppositeSegment`     INT,
  PRIMARY KEY (`magId`),
  KEY `idx_stake` (`stake`)
) ENGINE = InnoDB;

-------------------------------------------------------------
-- Tablas “hijas” (referencian map.magId)
-------------------------------------------------------------
CREATE TABLE `centerpos2x` (
  `magId`               INT NOT NULL,
  `stake`               VARCHAR(9),
  `lineId`              INT,
  `lineDirectionTypeId` INT,
  `xCoordinate`         INT,
  `yCoordinate`         INT,
  `pixelValue`          INT,
  `platformName`        INT,
  `platformNumber`      INT,
  PRIMARY KEY (`magId`),
  CONSTRAINT `fk_center_mag`
    FOREIGN KEY (`magId`) REFERENCES `map`(`magId`)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB;

CREATE TABLE `bamboopattern` (
  `magId`               INT NOT NULL,
  `stake`               VARCHAR(9),
  `siteNumber`          INT,
  `vehicleleft`         INT,
  `top`                 INT,
  `lineDirectionTypeId` INT,
  `lineId`              INT,
  `platformName`        INT,
  PRIMARY KEY (`magId`),
  CONSTRAINT `fk_bamboo_mag`
    FOREIGN KEY (`magId`) REFERENCES `map`(`magId`)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB;

CREATE TABLE `largescreenpixelpos` (
  `magId`               INT NOT NULL,
  `lineId`              INT,
  `lineDirectionTypeId` INT,
  `xCoordinate`         INT,
  `yCoordinate`         INT,
  `pixelValue`          INT,
  `platformName`        INT,
  `platformNumber`      INT,
  `stopTime`            DOUBLE,
  `residenceTime`       VARCHAR(32),
  PRIMARY KEY (`magId`),
  CONSTRAINT `fk_large_mag`
    FOREIGN KEY (`magId`) REFERENCES `map`(`magId`)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB;
