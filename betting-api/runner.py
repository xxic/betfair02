from models import Storage, Event
from base import Base

# initialize mysql storage
Storage().init_storage()

# get events
base = Base()
operation = 'listEvents/'
payload = '{"filter":{"eventTypeIds":["1"]}}'
data = base.retrieve(operation, payload)  # list of dicts
events = []
for event in data:
    events.append(Event(event))
