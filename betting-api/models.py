import mysql.connector
import maya

from base import Base

database = 'betting'
tables = {
    'event': '''
        CREATE TABLE IF NOT EXISTS `{}`.`event` (
          `event_id` INT NOT NULL,
          `event_name` VARCHAR(180) NOT NULL,
          `country_code` VARCHAR(5) NULL,
          `timezone` VARCHAR(45) NOT NULL,
          `open_date` VARCHAR(90) NOT NULL,
          `market_count` TINYINT NOT NULL,
          PRIMARY KEY (`event_id`),
          INDEX `event_name_idx` (`event_name` ASC) VISIBLE)
        ENGINE = InnoDB
    '''.format(database),
    'market': '''
        CREATE TABLE IF NOT EXISTS `{}`.`market` (
          `event_id` INT NOT NULL,
          `event_name` VARCHAR(180) NOT NULL,
          `market_id` FLOAT(10,9) NOT NULL,
          `market_name` VARCHAR(90) NOT NULL,
          `is_market_data_delayed` TINYINT NOT NULL,
          `status` VARCHAR(10) NOT NULL,
          `bet_delayed` TINYINT NOT NULL,
          `bsp_reconciled` TINYINT NOT NULL,
          `complete` TINYINT NOT NULL,
          `inplay` TINYINT NOT NULL,
          `number_of_winners` TINYINT NOT NULL,
          `number_of_runners` TINYINT NOT NULL,
          `number_of_active_runners` TINYINT NOT NULL,
          `total_matched` FLOAT(20,2) NOT NULL,
          `cross_matching` TINYINT NOT NULL,
          `runners_voidable` TINYINT NOT NULL,
          `version` BIGINT NOT NULL,
          PRIMARY KEY (`market_id`),
          INDEX `fk_event_id_idx` (`event_id` ASC) VISIBLE,
          INDEX `fk_event_name_idx` (`event_name` ASC) VISIBLE,
          INDEX `market_name_idx` (`market_name` ASC) VISIBLE,
          CONSTRAINT `market_fk_event_id`
            FOREIGN KEY (`event_id`)
            REFERENCES `{}`.`event` (`event_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `market_fk_event_name`
            FOREIGN KEY (`event_name`)
            REFERENCES `{}`.`event` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE)
        ENGINE = InnoDB
    '''.format(database, database, database),
    'runner': '''
        CREATE TABLE IF NOT EXISTS `{}`.`runner` (
          `event_id` INT NOT NULL,
          `event_name` VARCHAR(180) NOT NULL,
          `market_id` FLOAT(10,9) NOT NULL,
          `market_name` VARCHAR(90) NOT NULL,
          `selection_id` MEDIUMINT NOT NULL,
          `runner_name` VARCHAR(90) NOT NULL,
          `handicap` FLOAT(5,2) NOT NULL,
          `status` VARCHAR(10) NOT NULL,
          `total_matched` FLOAT(20,2) NOT NULL,
          INDEX `fk_event_id_idx` (`event_id` ASC) VISIBLE,
          INDEX `fk_event_name_idx` (`event_name` ASC) VISIBLE,
          INDEX `fk_market_id_idx` (`market_id` ASC) VISIBLE,
          INDEX `fk_market_name_idx` (`market_name` ASC) VISIBLE,
          INDEX `selection_id_idx` (`selection_id` ASC) VISIBLE,
          INDEX `runner_name_idx` (`runner_name` ASC) VISIBLE,
          CONSTRAINT `runner_fk_event_id`
            FOREIGN KEY (`event_id`)
            REFERENCES `{}`.`event` (`event_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `runner_fk_event_name`
            FOREIGN KEY (`event_name`)
            REFERENCES `{}`.`event` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `runner_fk_market_id`
            FOREIGN KEY (`market_id`)
            REFERENCES `{}`.`market` (`market_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `runner_fk_market_name`
            FOREIGN KEY (`market_name`)
            REFERENCES `{}`.`market` (`market_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE)
        ENGINE = InnoDB
    '''.format(database, database, database, database, database),
    'available_to_back': '''
        CREATE TABLE IF NOT EXISTS `{}`.`available_to_back` (
          `event_id` INT NOT NULL,
          `event_name` VARCHAR(180) NOT NULL,
          `market_id` FLOAT(10,9) NOT NULL,
          `market_name` VARCHAR(90) NOT NULL,
          `selection_id` MEDIUMINT NOT NULL,
          `runner_name` VARCHAR(90) NOT NULL,
          `price` FLOAT(5,2) NOT NULL,
          `size` FLOAT(20,2) NOT NULL,
          INDEX `fk_runner_name_idx` (`runner_name` ASC) VISIBLE,
          INDEX `fk_selection_id_idx` (`selection_id` ASC) VISIBLE,
          INDEX `fk_market_name_idx` (`market_name` ASC) VISIBLE,
          INDEX `fk_market_id_idx` (`market_id` ASC) VISIBLE,
          INDEX `fk_event_name_idx` (`event_name` ASC) VISIBLE,
          INDEX `fk_event_id_idx` (`event_id` ASC) VISIBLE,
          CONSTRAINT `avb_fk_event_id`
            FOREIGN KEY (`event_id`)
            REFERENCES `{}`.`event` (`event_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avb_fk_event_name`
            FOREIGN KEY (`event_name`)
            REFERENCES `{}`.`event` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avb_fk_market_id`
            FOREIGN KEY (`market_id`)
            REFERENCES `{}`.`market` (`market_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avb_fk_market_name`
            FOREIGN KEY (`market_name`)
            REFERENCES `{}`.`market` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avb_fk_selection_id`
            FOREIGN KEY (`selection_id`)
            REFERENCES `{}`.`runner` (`selection_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avb_fk_runner_name`
            FOREIGN KEY (`runner_name`)
            REFERENCES `{}`.`runner` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE)
        ENGINE = InnoDB
    '''.format(database, database, database, database, database, database, database),
    'available_to_lay': '''
        CREATE TABLE IF NOT EXISTS `{}`.`available_to_lay` (
          `event_id` INT NOT NULL,
          `event_name` VARCHAR(180) NOT NULL,
          `market_id` FLOAT(10,9) NOT NULL,
          `market_name` VARCHAR(90) NOT NULL,
          `selection_id` MEDIUMINT NOT NULL,
          `runner_name` VARCHAR(90) NOT NULL,
          `price` FLOAT(5,2) NOT NULL,
          `size` FLOAT(20,2) NOT NULL,
          INDEX `fk_runner_name_idx` (`runner_name` ASC) VISIBLE,
          INDEX `fk_selection_id_idx` (`selection_id` ASC) VISIBLE,
          INDEX `fk_market_name_idx` (`market_name` ASC) VISIBLE,
          INDEX `fk_market_id_idx` (`market_id` ASC) VISIBLE,
          INDEX `fk_event_name_idx` (`event_name` ASC) VISIBLE,
          INDEX `fk_event_id_idx` (`event_id` ASC) VISIBLE,
          CONSTRAINT `avl_fk_event_id`
            FOREIGN KEY (`event_id`)
            REFERENCES `{}`.`event` (`event_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avl_fk_event_name`
            FOREIGN KEY (`event_name`)
            REFERENCES `{}`.`event` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avl_fk_market_id`
            FOREIGN KEY (`market_id`)
            REFERENCES `{}`.`market` (`market_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avl_fk_market_name`
            FOREIGN KEY (`market_name`)
            REFERENCES `{}`.`market` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avl_fk_selection_id`
            FOREIGN KEY (`selection_id`)
            REFERENCES `{}`.`runner` (`selection_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
          CONSTRAINT `avl_fk_runner_name`
            FOREIGN KEY (`runner_name`)
            REFERENCES `{}`.`runner` (`event_name`)
            ON DELETE CASCADE
            ON UPDATE CASCADE)
        ENGINE = InnoDB
    '''.format(database, database, database, database, database, database, database)
}

runner_data = {}


class Storage(Base):

    def __init__(self):
        super().__init__()

    def init_storage(self):
        try:
            connection = mysql.connector.connect(**self.mysql_credentials)
            cursor = connection.cursor()
            print('creating database {}...'.format(database))
            cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(database))
            for key, value in tables.items():
                print(' > creating table {}..'.format(key))
                cursor.execute(value)
            connection.commit()
        except mysql.connector.Error as error:
            print('[Event -> create_table]:', error)


class Event(Base):
    query = 'INSERT INTO `{}`.`event` (`event_id`, `event_name`, `country_code`, `timezone`, `open_date`, ' \
            '`market_count`) ' \
            'VALUES (%s, %s, %s, %s, %s, %s);'.format(database)

    def __init__(self, data: dict = None):
        super().__init__()
        self.table = tables['event']
        if data is not None:
            self.data = data

            self.event_id = data['event']['id']
            self.event_name = data['event']['name']
            try:
                self.country_code = data['event']['countryCode']
            except KeyError:
                self.country_code = ''
            self.timezone = data['event']['timezone']
            self.open_date = data['event']['openDate']
            self.market_count = data['marketCount']

            self.insert()

            # get market catalogue
            operation = 'listMarketCatalogue/'
            payload = '{"filter":{"eventIds":["' + self.event_id + \
                      '"]},"maxResults":"50","marketProjection":["RUNNER_METADATA"]}'
            catalogue_data = self.retrieve(operation, payload)
            self.markets = []
            for catalogue in catalogue_data:
                operation = 'listMarketBook/'
                payload = '{"marketIds":["' + catalogue['marketId'] + '"]}'
                market_data = self.retrieve(operation, payload)
                self.markets.append(Market(self.event_id, self.event_name, catalogue, market_data))

    def insert(self):
        values = (self.event_id, self.event_name, self.country_code, self.timezone, self.open_date, self.market_count)
        try:
            connection = mysql.connector.connect(**self.mysql_credentials)
            cursor = connection.cursor()
            print('..updating events [{}]'.format(self.event_name))
            cursor.execute(self.query, values)
            connection.commit()
        except mysql.connector.Error as error:
            print('ERR [Event -> insert][{}]:'.format(self.event_name), error)


class Market(Base):
    query = 'INSERT INTO `{}`.`market` (`event_id`, `event_name`, `market_id`, `market_name`, ' \
            '`is_market_data_delayed`, `status`, `bet_delayed`, `bsp_reconciled`, `complete`, `inplay`, ' \
            '`number_of_winners`, `number_of_runners`, `number_of_active_runners`, `total_matched`, ' \
            '`cross_matching`, `runners_voidable`, `version`) ' \
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'.format(database)

    def __init__(self, ev_id, ev_name, market_catalogue: dict, market_book: dict):
        super().__init__()
        self.ev_id = ev_id
        self.ev_name = ev_name

        # get selection_id and runner_name from market market_catalogue
        for runner in market_catalogue['runners']:
            runner_data[runner['selectionId']] = runner['runnerName']

        # get other market values from market_book
        self.market_id = market_book[0]['marketId']
        print(self.market_id)
        self.market_name = market_catalogue['marketName']
        self.is_market_data_delayed = market_book[0]['isMarketDataDelayed']
        self.status = market_book[0]['status']
        self.bet_delay = market_book[0]['betDelay']
        self.bsp_reconciled = market_book[0]['bspReconciled']
        self.complete = market_book[0]['complete']
        self.inplay = market_book[0]['inplay']
        self.number_of_winners = market_book[0]['numberOfRunners']
        self.number_of_runners = market_book[0]['numberOfActiveRunners']
        self.number_of_active_runners = market_book[0]['numberOfActiveRunners']
        self.total_matched = market_book[0]['totalMatched']
        self.total_available = market_book[0]['totalAvailable']
        self.cross_matching = market_book[0]['crossMatching']
        self.runners_voidable = market_book[0]['runnersVoidable']
        self.version = market_book[0]['version']

        self.insert()

        # initialize runner

    def insert(self):
        values = (self.ev_id, self.ev_name, self.market_id, self.market_name, self.is_market_data_delayed,
                  self.status, self.bet_delay, self.bsp_reconciled, self.complete, self.inplay,
                  self.number_of_winners, self.number_of_runners, self.number_of_active_runners,
                  self.total_matched, self.cross_matching, self.runners_voidable, self.version)
        try:
            connection = mysql.connector.connect(**self.mysql_credentials)
            cursor = connection.cursor()
            print('  ..updating markets [{}]'.format(self.market_name))
            cursor.execute(self.query, values)
            connection.commit()
        except mysql.connector.Error as error:
            print('ERR [Market -> insert][{}]:'.format(self.market_name), error)


class Runner:

    def __init__(self, data: dict):
        pass
