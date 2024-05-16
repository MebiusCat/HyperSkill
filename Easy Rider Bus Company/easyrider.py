"""aaaaa """

import json
import enum
import re
from itertools import groupby


class BusStop(enum.Enum):
    stop_S = 'S'
    stop_O = 'O'
    stop_F = 'F'


class BusLine:
    def __init__(self, bus_number):
        self.bus_number = bus_number
        self.start_point = None
        self.finish_point = None
        self.transfer = []

    def add_station(self, name, stop_type, a_time) -> None:
        if stop_type == BusStop.stop_S.value:
            if not self.start_point:
                self.start_point = name
        if stop_type == BusStop.stop_F.value:
            if not self.finish_point:
                self.finish_point = name
        self.transfer.append((name, a_time, stop_type))

    def __repr__(self):
        return f"{self.bus_number} {self.transfer}"


class ErrorDetector:
    bus_lines: dict[str, BusLine]

    def __init__(self) -> None:
        self.bus_id = 0
        self.stop_id = 0
        self.stop_name = 0
        self.next_stop = 0
        self.stop_type = 0
        self.a_time = 0

        self.stop_list = {}
        self.validation_succeed = True
        self.bus_lines = {}

    @staticmethod
    def valid_bus_id(bus_id):
        return \
            isinstance(bus_id, int)

    @staticmethod
    def valid_stop_id(stop_id):
        return\
            isinstance(stop_id, int)

    @staticmethod
    def valid_stop_name(stop_name):
        return \
            (isinstance(stop_name, str)
             and re.match(r"^[A-Z][\w\s]+ (Road|Avenue|Boulevard|Street)$", stop_name))

    @staticmethod
    def valid_next_stop(next_stop):
        return \
            isinstance(next_stop, int)

    @staticmethod
    def valid_stop_type(stop_type):
        return \
            True if not stop_type else stop_type in ('S', 'O', 'F')

    @staticmethod
    def valid_a_time(a_time):

        return \
            (isinstance(a_time, str)
             and re.match(r"(0\d|1\d|2[0-3]):[0-5]\d$", a_time))

    def check(self, json_data) -> None:
        for el in json_data:
            self.bus_id += not (
                ErrorDetector.valid_bus_id(el["bus_id"]))
            self.stop_id += not (
                ErrorDetector.valid_stop_id(el["stop_id"]))
            self.stop_name += not (
                ErrorDetector.valid_stop_name(el["stop_name"]))
            self.next_stop += not (
                ErrorDetector.valid_next_stop(el["next_stop"]))
            self.stop_type += not (
                ErrorDetector.valid_stop_type(el["stop_type"]))
            self.a_time += not (
                ErrorDetector.valid_a_time(el["a_time"]))

            if el["bus_id"] not in self.stop_list:
                self.stop_list[el["bus_id"]] = []
            if el["stop_id"] not in self.stop_list[el["bus_id"]]:
                self.stop_list[el["bus_id"]].append(el["stop_id"])

            if el["bus_id"]:
                if not el["bus_id"] in self.bus_lines:
                    self.bus_lines[el["bus_id"]] = BusLine(el["bus_id"])
                self.bus_lines[el["bus_id"]]\
                    .add_station(el["stop_name"], el["stop_type"], el["a_time"])

    def check_route(self) -> None:
        gen_start = []
        gen_finish = []
        gen_transfer = []
        _transfer = []

        for num, line in self.bus_lines.items():
            if not line.start_point or not line.finish_point:
                print(f"There is no start or end stop for the line: {num}.")
                return
            if line.start_point not in gen_start:
                gen_start.append(line.start_point)

            if line.finish_point not in gen_finish:
                gen_finish.append(line.finish_point)

            for name, _, _ in line.transfer:
                _transfer.append(name)

        _transfer.sort()
        for k, v in groupby(_transfer):
            if len(list(v)) > 1:
                gen_transfer.append(k)

        print(f"Start stops: {len(gen_start)}", sorted(gen_start))
        print(f"Transfer stops: {len(gen_transfer)}", sorted(gen_transfer))
        print(f"Finish stops: {len(gen_finish)}", sorted(gen_finish))


    def check_a_time(self) -> None:
        print("Arrival time test:")
        broken_time = False
        for num, line in self.bus_lines.items():
            prev_date = None
            for name, cur_date, _ in line.transfer:
                if prev_date and prev_date >= cur_date:
                    print(f"bus_id line {num}: wrong time on station {name}")
                    broken_time = True
                    break
                prev_date = cur_date
        if not broken_time:
            print("OK")


    def check_on_demand(self) -> None:
        print("On demand stops test:")
        on_demand = {}
        error = []
        for num, line in self.bus_lines.items():
            for name, _, s_type in line.transfer:
                if name in on_demand:
                    if on_demand[name] != (s_type == 'O'):
                        if name not in error:
                            error.append(name)
                else:
                    on_demand[name] = (s_type == 'O')
        if error:
            print(f"Wrong stop type: ", sorted(error))
        else:
            print("OK")


    def bus_station_counter(self) -> None:
        print("Line names and number of stops:")
        for k, v in sorted(self.stop_list.items(), key=lambda el: (el[0], el[1])):
            print(f"bus_id: {k}, stops: {len(v)}")

    def report(self) -> None:
        print(f"""Type and required field validation: {self.all_errors()} errors
bus_id: {self.bus_id}
stop_id: {self.stop_id}
stop_name: {self.stop_name}
next_stop: {self.next_stop}
stop_type: {self.stop_type}
a_time: {self.a_time}""")

    def validation(self) -> None:
        print(f"Format validation: {self.validation_errors()} errors")
        print(f"stop_name: {self.stop_name}")
        print(f"stop_type: {self.stop_type}")
        print(f"a_time: {self.a_time}")

    def all_errors(self) -> int:
        return (self.bus_id +
                self.stop_id +
                self.stop_name +
                self.next_stop +
                self.stop_type +
                self.a_time)

    def validation_errors(self) -> int:
        return (self.stop_name +
                self.stop_type +
                self.a_time)

# my_str = input()

my_str = """[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "O",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": 256,
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "09:20"
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]
"""

# my_str = """
# [
#     {
#         "bus_id": 512,
#         "stop_id": 4,
#         "stop_name": "Bourbon Street",
#         "next_stop": 6,
#         "stop_type": "S",
#         "a_time": "08:13"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:16"
#     }
# ]"""

data = json.loads(my_str)
checker = ErrorDetector()
checker.check(data)
checker.bus_station_counter()
checker.check_route()
checker.check_a_time()
checker.check_on_demand()