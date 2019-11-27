from operations import Operations, OperationsSQL

ops = Operations()

operation = 'listEvents/'
payload = '{"filter":{"eventTypeIds":["1"]}}'
data = ops.retrieve(operation, payload)

ops_sql = OperationsSQL(data)

ops_sql.list_events_sql()
