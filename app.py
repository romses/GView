from logbook import Logbook


lb = Logbook("test.gl")
events = lb.get_all_events()

for event in events:
    print(event.data)
    print(event.metadata)