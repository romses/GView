from logbook import Logbook


lb = Logbook("test.gl")

for event in lb.events:
    print(event.metadata)
    print(event.data)


#lb.import_file("723H3126.FIT")