from base import Base

import mysql.connector
import time


class Operations(Base):
    dbname = 'betting'

    tables = {
        'events': '''
        CREATE TABLE IF NOT EXISTS `betting`.`events` (
          `eventId` INT NOT NULL,
          `eventName` VARCHAR(180) NOT NULL,
          `countryCode` VARCHAR(5) NULL,
          `timezone` VARCHAR(45) NOT NULL,
          `openDate` DATETIME NOT NULL,
          `marketCount` INT NOT NULL,
          PRIMARY KEY (`eventId`))
        ENGINE = InnoDB
        ''',
        'markets': '''
        CREATE TABLE IF NOT EXISTS `betting`.`markets` (
          `eventId` INT NOT NULL,
          `eventName` VARCHAR(180) NULL,
          `marketId` FLOAT(20,19) NOT NULL,
          `marketName` VARCHAR(180) NOT NULL,
          `totalMatched` FLOAT(10,2) NOT NULL,
          `status` TINYINT NOT NULL,
          `version` BIGINT NOT NULL,
          PRIMARY KEY (`marketId`),
          INDEX `fk_eventId_idx` (`eventId` ASC) VISIBLE,
          CONSTRAINT `fk_eventId`
            FOREIGN KEY (`eventId`)
            REFERENCES `betting`.`events` (`eventId`)
            ON DELETE CASCADE
            ON UPDATE CASCADE)
        ENGINE = InnoDB
        ''',
        'runners': '''
        CREATE TABLE IF NOT EXISTS `betting`.`runners` (
          `eventName` VARCHAR(180) NULL,
          `marketId` FLOAT(20,19) NOT NULL,
          `selectionId` INT NOT NULL,
          `runnerName` VARCHAR(90) NOT NULL,
          `handicap` FLOAT(6,3) NOT NULL,
          `status` TINYINT NOT NULL,
          `lastPriceTraded` FLOAT(10,2) NULL,
          `totalMatched` FLOAT(10,2) NULL,
          INDEX `fk_marketId_idx` (`marketId` ASC) VISIBLE,
          CONSTRAINT `fk_marketId`
            FOREIGN KEY (`marketId`)
            REFERENCES `betting`.`markets` (`marketId`)
            ON DELETE CASCADE
            ON UPDATE CASCADE)
        ENGINE = InnoDB
        '''
    }

    events_query = 'insert into `{}`.`events` (`eventId`, `eventName`, `countryCode`, `timezone`, `openDate`, ' \
                   '`marketCount`) ', 'values (%s, %s, %s, %s, %s, %s)'.format(dbname)

    def __init__(self):
        super().__init__()
        # Initialize database and tables
        try:
            connection = mysql.connector.connect(**self.mysql_credentials)
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(self.dbname))
            for key, value in self.tables.items():
                print('create {} table..'.format(key))
                cursor.execute(value)
            connection.commit()
        except mysql.connector.Error as error:
            print(error)

    def list_events_sql(self):
        try:
            connection = mysql.connector.connect(**self.mysql_credentials)
            cursor = connection.cursor()

            for entry in self.data:
                if ' v ' in entry['event']['name']:
                    try:
                        country_code = entry['event']['countryCode']
                    except KeyError:
                        country_code = ''
                    print('..updating:', entry['event']['name'])
                    try:
                        cursor.execute(self.events_query,
                                       (entry['event']['id'], entry['event']['name'], country_code,
                                        entry['event']['timezone'], entry['event']['openDate'], entry['marketCount']))
                    except mysql.connector.Error as error:
                        print(error)

            connection.commit()

        except mysql.connector.Error as error:
            print(error)

    def list_market_catalogue_sql(self):
        pass
