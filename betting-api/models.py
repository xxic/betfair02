from base import Base


class Event(Base):

    def __init__(self, data: dict):
        super().__init__()
        """
        :param data:
        """
        for key, value in data.items():
            if key == 'event':
                for foo, bar in value.items():
                    if foo == 'id':
                        self.event_id = bar
                    if foo == 'name':
                        self.event_name = bar
                    if foo == 'countryCode':
                        self.country_code = bar
                    if foo == 'timezone':
                        self.timezone = bar
                    if foo == 'openDate':
                        self.open_date = bar
            if key == 'marketCount':
                self.market_count = value
        # todo: commit to event table

        operation = 'listMarketCatalogue/'
        payload = '{"filter":{"eventIds":["' + self.event_id + \
                  '"]},"maxResults":"50","marketProjection":["RUNNER_METADATA"]}'
        response = self.retrieve(operation, payload)

        # initialize markets
        self.markets = []
        for item in response:
            market = Market(item)
            self.markets.append(market)


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
