import base64
import inspect
import json
import random
import warnings
from enum import StrEnum
from typing import Union

log: dict[str, list] = {"creationEvents": [], "callEvents": [], "recievedEvents": [], "deregisterEvents": []}


def b64Encode(what: str) -> str:
    return base64.b64encode(what.encode("utf-8")).decode("utf-8")


class customObservable:
    def __init__(self, name) -> None:
        global observers
        raise NotImplementedError("Not Implemented")
        self.name = name
        observers[name] = {"gained": [], "time": [], "all": [], "other": []}


class Observable(StrEnum):
    ITEM_OBSERVABLE = "itemObserv"
    # Will be called when an item is gained manually, and will be called every 5 seconds with the current item amounts
    ACHEVEMENT_OBSERVABLE = "acheObserv"
    # Will be called when an achevement is earned
    AUTOMATION_OBSERVABLE = "autoObserv"
    # Will be called when an Automation is gained manually, and will be called every 5 seconds with the current level counts
    TIME_OBSERVABLE = "timeObserv"
    # Will be called every 5 seconds
    OTHER_OBSERVABLE = "otherObserv"
    # Probably will not be used. For any other observable not specific enough to fit in a single catagory
    # But in that case, it will most likely get it's own observable.
    RESET_OBSERVABLE = "resetObserv"
    # This will be called when a tab needs to be reloaded. It will be called with the name of the tab to reset.
    UNLOCK_OBSERVABLE = "unlockObserv"
    # This will be called when a new thing is unlocked. It will be called with the name of the thing unlocked.


class ObservableCallType(StrEnum):
    # What to call on
    GAINED = "gained"
    TIME = "time"
    ALL = "all"
    OTHER = "other"


class ObservableCheckType(StrEnum):
    # AMOUNT = "amount"
    TYPE = "type"


"""
Bootleg implementation of the obeserver model.
There will be a list of observers: List[tuple(function, string, string, (string, string))]. The function is the function to call, the string is which event to
call the function on, the third string is what type of event to call on, and the fourth item is a tuple containing a check type, and the second string is what to check for.

Observables and their documentation are defined in the class above.
"""
observers: dict = {}
for event in Observable:
    observers[str(event)] = {"gained": [], "time": [], "all": [], "other": []}


class observer:
    def __init__(
        self,
        function_,
        event: Observable,
        callType: ObservableCallType,
        checkType: ObservableCheckType | None = None,
        check: str | None = None,
    ) -> None:
        self.function = function_
        self.event = event
        self.callType = callType
        self.checkType = checkType
        self.check = check
        self.id = b64Encode(
            json.dumps({"what": event, "calltype": callType, "randInt": str(random.randint(10000, 99999))})
        )

        log["creationEvents"].append(self.id)

    def deregister(self) -> None:
        matchingObservers: list[observer] = observers[self.event][self.callType]

        for i in range(len(matchingObservers)):
            if matchingObservers[i].id == self.id:
                matchingObservers.pop(i)

                log["deregisterEvents"].append(self.id)
                del self  # o7 to the observer

                return

        warnings.warn(f"Observer for {self.event} on {self.callType} with id {self.id} not found")


def registerObserver(
    function_,
    event: Observable,
    callType: ObservableCallType,
    checkType: ObservableCheckType | None = None,
    check: str | None = None,
) -> observer:
    print(f"new observer for {event} when {callType} occurs")

    if not event in Observable:
        raise TypeError("Incorrect type for what to call on, it should be a Enum from Observable")
    if not callType in ObservableCallType:
        raise TypeError("Incorrect type for callType. Use the ObservableCallType enum.")
    if not type(checkType) == ObservableCheckType and not checkType == None:
        raise TypeError("Incorrect type for checkType, it should use the ObservableCheckType enum")
    if not type(check) == str and not check == None:
        raise TypeError(f"Check should be a str")

    sig = str(inspect.signature(function_)).split(",")  # amount of arguments
    if not len(sig) >= 1:
        raise TypeError("Function should have at least one argument")

    if not event in observers:
        observers[event] = {"gained": [], "time": [], "all": [], "other": []}

    newObserver = observer(function_, event, callType, checkType, check)

    observers[event][callType].append(newObserver)

    return newObserver


def callEvent(event: Observable, callType: ObservableCallType, information: Union[str, tuple, int]):
    """
    Function to call an event
    """
    if not callType == "time":
        print("Calling event " + event)

    if not callType in ObservableCallType:
        raise TypeError("Incorrect type for callType. Use the ObservableCallType enum.")
    if not event in Observable:
        raise TypeError("Incorrect type for what to call, it should be a enum from Observable")

    item: observer
    somebodyRecieved = False

    for item in observers[event]["all"]:  # for every observer that has the correct event type and all calltypes
        if item.checkType == ObservableCheckType.TYPE:
            if information == item.check:
                log["recievedEvents"].append(item.id)
                item.function(information)
                somebodyRecieved = True

        else:
            log["recievedEvents"].append(item.id)
            item.function(information)

    for item in observers[event][callType]:  # for every observer that has the correct call type and event type
        if item.checkType == ObservableCheckType.TYPE:
            if information == item.check:
                log["recievedEvents"].append(item.id)
                item.function(information)
                somebodyRecieved = True

        else:
            log["recievedEvents"].append(item.id)
            item.function(information)  # if there is no check
            somebodyRecieved = True

    if not somebodyRecieved:
        log["recievedEvents"].append(None)

    log["callEvents"].append({"event": event, "callType": callType, "information": information})
