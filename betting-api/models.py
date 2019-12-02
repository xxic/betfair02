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
          `market_id` FLOAT(20,19) NOT NULL,
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
          `market_id` FLOAT(20,19) NOT NULL,
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
          `market_id` FLOAT(20,19) NOT NULL,
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
          `market_id` FLOAT(20,19) NOT NULL,
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

            # pass to market
            self.markets = []
            #
            operation = ''

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

    def __init__(self, data: dict):
        """
        :param data:
        """
        super().__init__()
        for key, value in data.items():
            if key == 'marketId':
                self.market_id = value
            if key == 'marketName':
                self.market_name = value
            if key == 'totalMatched':
                self.total_matched = value

        operation = 'listMarketBook/'
        payload = '{"marketIds":["' + self.market_id + '"]}'
        response = self.retrieve(operation, payload)

        for key, value in response[0].items():
            if key == 'status':
                self.status = value
            if key == 'totalAvailable':
                self.total_available = value
            if key == 'version':
                self.version = value
        # todo: commit to markets table

        # initialize runners
        self.runners = []
        for item in response[0]['runners']:
            runner = Runner(item)
            self.runners.append(runner)


class Runner:

    def __init__(self, data: dict):
        """
        :param data:
        """
        for key, value in data.items():
            if key == 'selectionId':
                self.selection_id = value
            if key == 'handicap':
                self.selection_id = value
            if key == 'status':
                self.status = value
            if key == 'totalMatched':
                self.total_matched = value
