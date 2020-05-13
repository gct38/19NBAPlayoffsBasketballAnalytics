#class to help better organize all Event Codes
class EventCodes:
    def __init__(self, EventCodesLine):
        self.eventMsg = dict()
        self.eventMsg[int(EventCodesLine[0].strip())] = str(EventCodesLine[2]).strip()
        self.actionType = dict()
        self.actionType[int(EventCodesLine[1].strip())] = str(EventCodesLine[3]).strip()

    def print(self):
        print(self.__str__())

    def __str__(self):
        message = ""
        for key in self.eventMsg:
            message += "Event Message: " + self.eventMsg[key] + ","
        for key in self.actionType:
            message += " Action Type: " + self.actionType[key]
        return message


#search function that returns an EventCodes object
def searchEventCodes(eventCodes, eventMsg, actionType):
    eventMsg = int(eventMsg)
    actionType = int(actionType)
    for event in eventCodes:
        if eventMsg in event.eventMsg and actionType in event.actionType:
            return event
        else:
            continue
    return None