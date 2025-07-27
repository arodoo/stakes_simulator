"""
Database schema management service.
Handles table creation and deletion operations.
"""

from sqlalchemy import text
from typing import List


class DatabaseSchemaService:
    """Service for managing database schema operations."""
    
    def __init__(self, engine):
        self.engine = engine
    
    def drop_tables_if_exist(self, table_names: List[str]) -> None:
        """Drop tables if they exist, in reverse order for FK constraints."""
        with self.engine.begin() as conn:
            conn.execute(text("SET foreign_key_checks = 0;"))
            
            for table in reversed(table_names):
                conn.execute(text(f"DROP TABLE IF EXISTS `{table}`;"))
                print(f"Dropped table: {table}")
            
            conn.execute(text("SET foreign_key_checks = 1;"))
    
    def create_tables(self) -> None:
        """Create all required tables."""
        with self.engine.begin() as conn:
            self._create_map_table(conn)
            self._create_centerpos2x_table(conn)
            self._create_bamboopattern_table(conn)
            self._create_largescreenpixelpos_table(conn)
            print("All tables created successfully")
    
    def _create_map_table(self, conn) -> None:
        """Create the main map table."""
        sql = """
        CREATE TABLE `map` (
            `magId` INT NOT NULL,
            `segment` INT,
            `lineDirectionTypeId` INT,
            `stake` VARCHAR(9),
            `type` DOUBLE,
            `epc` VARCHAR(24),
            `tid` DOUBLE,
            `polar` TINYINT,
            `hidenEnable` TINYINT,
            `transverse` DOUBLE,
            `longitudinal` DOUBLE,
            `curvature` DOUBLE,
            `coordinateX` DOUBLE,
            `coordinateY` DOUBLE,
            `coordinateE` INT,
            `coordinateN` INT,
            `cruisingSpeed` INT,
            `limitSpeed` INT,
            `scene` TINYINT,
            `stationType` DOUBLE,
            `stationNum` INT,
            `signallamp` TINYINT,
            `oneWayRoad` TINYINT,
            `meetingVec` TINYINT,
            `oppositeSegment` INT,
            PRIMARY KEY (`magId`),
            KEY `idx_stake` (`stake`)
        ) ENGINE = InnoDB;
        """
        conn.execute(text(sql))
    
    def _create_centerpos2x_table(self, conn) -> None:
        """Create centerpos2x table."""
        sql = """
        CREATE TABLE `centerpos2x` (
            `magId` INT NOT NULL,
            `stake` VARCHAR(9),
            `lineId` INT,
            `lineDirectionTypeId` INT,
            `xCoordinate` INT,
            `yCoordinate` INT,
            `pixelValue` INT,
            `platformName` INT,
            `platformNumber` INT,
            PRIMARY KEY (`magId`),
            CONSTRAINT `fk_center_mag`
                FOREIGN KEY (`magId`) REFERENCES `map`(`magId`)
                ON UPDATE CASCADE ON DELETE RESTRICT
        ) ENGINE = InnoDB;
        """
        conn.execute(text(sql))
    
    def _create_bamboopattern_table(self, conn) -> None:
        """Create bamboopattern table."""
        sql = """
        CREATE TABLE `bamboopattern` (
            `magId` INT NOT NULL,
            `stake` VARCHAR(9),
            `siteNumber` INT,
            `vehicleleft` INT,
            `top` INT,
            `lineDirectionTypeId` INT,
            `lineId` INT,
            `platformName` INT,
            PRIMARY KEY (`magId`),
            CONSTRAINT `fk_bamboo_mag`
                FOREIGN KEY (`magId`) REFERENCES `map`(`magId`)
                ON UPDATE CASCADE ON DELETE RESTRICT
        ) ENGINE = InnoDB;
        """
        conn.execute(text(sql))
    
    def _create_largescreenpixelpos_table(self, conn) -> None:
        """Create largescreenpixelpos table."""
        sql = """
        CREATE TABLE `largescreenpixelpos` (
            `magId` INT NOT NULL,
            `lineId` INT,
            `lineDirectionTypeId` INT,
            `xCoordinate` INT,
            `yCoordinate` INT,
            `pixelValue` INT,
            `platformName` INT,
            `platformNumber` INT,
            `stopTime` DOUBLE,
            `residenceTime` VARCHAR(32),
            PRIMARY KEY (`magId`),
            CONSTRAINT `fk_large_mag`
                FOREIGN KEY (`magId`) REFERENCES `map`(`magId`)
                ON UPDATE CASCADE ON DELETE RESTRICT
        ) ENGINE = InnoDB;
        """
        conn.execute(text(sql))
