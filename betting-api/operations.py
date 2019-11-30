from base import Base

import requests
import mysql.connector


class Operations(Base):

    def __init__(self):
        super().__init__()

    def retrieve(self, operation, payload):
        """
        Generic method hat retrieves data based on the operation and filter supplied.
        :param operation: Betting API operation, for example; listEvents/
        :param payload: Filter
        :return: Operation-type data
        """
        headers = {
            'X-Application': self.application_key,
            'X-Authentication': self.token,
            'Content-Type': 'application/json'
        }
        return requests.request('post', self.rest_endpoint + operation, data=payload, headers=headers).json()


class OperationsSQL(Base):
    """
    Data handling for Operations
    """

    dbname = 'betting'
    tables = {'events': (
        "CREATE TABLE IF NOT EXISTS `{}`.`events` ("
        "  `id` INT NOT NULL,"
        "  `name` VARCHAR(180) NOT NULL,"
        "  `countryCode` VARCHAR(45) NULL,"
        "  `timezone` VARCHAR(45) NULL,"
        "  `openDate` VARCHAR(45) NULL,"
        "  `marketCount` INT NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB".format(dbname))}
    query = 'insert into `{}`.`events` (`id`, `name`, `countryCode`, `timezone`, `openDate`, `marketCount`) ' \
            'values (%s, %s, %s, %s, %s, %s)'.format(dbname)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def list_events_sql(self):
        try:
            connection = mysql.connector.connect(**self.mysql_credentials)
            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(self.dbname))
            cursor.execute(self.tables['events'])

            for entry in self.data:
                if ' v ' in entry['event']['name']:
                    try:
                        country_code = entry['event']['countryCode']
                    except KeyError:
                        country_code = ''
                    print('..updating:', entry['event']['name'])
                    try:
                        cursor.execute(self.query,
                                       (entry['event']['id'], entry['event']['name'], country_code,
                                        entry['event']['timezone'], entry['event']['openDate'], entry['marketCount']))
                    except mysql.connector.Error as error:
                        print(error)

            connection.commit()

        except mysql.connector.Error as error:
            print(error)

    def list_market_catalogue_sql(self):
        pass
