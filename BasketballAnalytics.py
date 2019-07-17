import csv

#TODO: create some type of data structure that'll hold the game_lineup data, just create a parsing func that will return some type of data structure

#class to help better organize all Event Codes
class EventCodes:
    def __init__(self, EventCodesLine):
        self.eventMsg = dict()
        self.eventMsg[int(EventCodesLine[0])] = str(EventCodesLine[2]).strip()
        self.actionType = dict()
        self.actionType[int(EventCodesLine[1])] = str(EventCodesLine[3]).strip()


def parseEventCodes(filename):
    eventCodes = list()
    filename = open(filename, encoding = "ISO-8859-1")
    filename.readline()
    for line in filename:
        line = line.replace("\"","").strip().split("\t")
        if len(line) < 4:
            line.append("")
        eventCodes.append(EventCodes(line))
    return eventCodes

#returns a EventCodes object
def searchEventCodes(eventCodes, eventMsg, actionType):
    eventMsg = int(eventMsg)
    actionType = int(actionType)
    for event in eventCodes:
        if eventMsg in event.eventMsg and actionType in event.actionType:
            return event
        else:
            continue
    return None





if __name__ == "__main__":
    ##testing area
    eventCodes = parseEventCodes("Event_Codes.txt")
    event = searchEventCodes(eventCodes, 15,32)
    if event != None:
        print(event.eventMsg)
        print(event.actionType)
    else:
        print("could not find")


