from operations import Operations, OperationsSQL

ops = Operations()

operation = 'listEvents/'
payload = '{"filter":{"eventTypeIds":["1"]}}'
data = ops.retrieve(operation, payload)
ops_sql = OperationsSQL(data)
# ops_sql.list_events_sql()
#
#
# operation = 'listMarketCatalogue/'
# for entry in data:
#     if ' v ' in entry['event']['name']:
#         payload = '{"filter":{"eventIds":["' + entry['event']['id'] + '"]},"sort":"MAXIMUM_TRADED","maxResults":"50",' \
#                                                                       '"marketProjection":["RUNNER_DESCRIPTION"]}'
#         data1 = ops.retrieve(operation, payload)
#         print(data1)
