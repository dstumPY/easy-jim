import json
import typing
from datetime import date, time, datetime, timedelta


def cast_valid_date(input_date: str) -> date:
    # assert input is separated by
    assert (
        len(input_date.split(".")) == 3
    ), f"WRONG DATE FORMAT - Input date must be separated by dots. Input was: {input_date}"
    date_split = input_date.split(".")

    # check int type of split parts
    try:
        day = int(date_split[0])
        month = int(date_split[1])
        year = int(date_split[2])
    except ValueError as error:
        print(error)
        raise Exception("Date string must contain only digits.")
    except IndexError as error:
        print(error)
        raise Exception(
            "WRONG DATE FORMAT - Input date must contain digits, separated by dots."
        )

    # check if input builts a valid date
    try:
        result_date = date(year, month, day)
    except ValueError as error:
        print(error)
        raise Exception(f"No valid date. Input date was {input_date}")

    return result_date


def cast_valid_time(input_time: str) -> time:
    assert (
        2 <= len(input_time.split(":")) <= 3
    ), f"WRONG TIME FORMAT - Input time must be separated by colons, e.g. 17:00. Input was: {input_time}"
    time_split = input_time.split(":")

    #
    try:

        if len(time_split) < 2:
            raise Exception(
                f"WRONG TIME FORMAT - Input time must be separated by colon, e.g. 17:00. Input was: {input_time}"
            )
        elif len(time_split) == 2:
            hour = int(time_split[0])
            minute = int(time_split[1])
            second = 0
        elif len(time_split) == 3:
            hour = int(time_split[0])
            minute = int(time_split[1])
            second = int(time_split[2])
    except ValueError as error:
        print(error)
        raise Exception("Date string must contain only digits.")

    try:
        result_time = time(hour, minute, second)
    except ValueError as error:
        print(error)
        raise Exception(f"No valid time. Input date was {input_time}")

    return result_time


def load_config(json_path: str) -> typing.Dict[str, typing.List]:
    with open(json_path) as json_data_file:
        data = json.load(json_data_file)

    for key, value in data.items():
        # iterate one-time-event list
        if key == "one-time-events":
            for event in value:
                # skip event when exception is thrown
                try:
                    event["start-date"] = cast_valid_date(event["start-date"])
                    event["end-date"] = cast_valid_date(event["end-date"])
                    event["start-time"] = cast_valid_time(event["start-time"])
                    event["end-time"] = cast_valid_time(event["end-time"])
                    # add repitition rhythm of zero days
                    event["rhythm"] = 0
                except:
                    del event
                    print(
                        "Warning: Event data can not be processed. Event was skipped."
                    )
                    continue
        # iterate multiple-times-events list
        elif key == "multiple-times-events":
            for event in value:
                try:
                    event["start-date"] = cast_valid_date(event["start-date"])
                    event["end-date"] = cast_valid_date(event["end-date"])
                    event["start-time"] = cast_valid_time(event["start-time"])
                    event["end-time"] = cast_valid_time(event["end-time"])
                    event["rhythm"] = int(event["rhythm"])
                except:
                    del event
                    print(
                        "Warning: Event data can not be processed. Event was skipped."
                    )
                    continue

    # return only event items
    event_list = data["one-time-events"] + data["multiple-times-events"]

    return event_list


def calc_dates_from_event(
    event_config: typing.Dict[str, typing.List],
    date_range_from: date,
    date_range_to: date,
) -> typing.List[typing.Dict]:

    # cast start and end to datetime for range the events needs
    # to be calculated for
    datetime_range_to = datetime.combine(date_range_to, time(23, 59, 59))
    datetime_range_from = datetime.combine(date_range_from, time(0, 0, 0))

    event_list = []
    for event_item in event_config:
        tmp_dic = {}
        # combine date and times from event_items to datetimes
        event_datetime_start = datetime.combine(
            event_item["start-date"], event_item["start-time"]
        )
        event_datetime_end = datetime.combine(
            event_item["end-date"], event_item["end-time"]
        )

        # for single events rhythm days is 0 and no other event dates need to be calculated
        if event_item["rhythm"] != 0:
            # how many times can rhythm days be added to start-date
            iteration_range = int(
                (datetime_range_to - event_datetime_start).days / event_item["rhythm"]
            )
            date_list = [
                {
                    "name": event_item["name"],
                    "from": event_datetime_start
                    + timedelta(days=i * event_item["rhythm"]),
                    "to": event_datetime_end + timedelta(days=i * event_item["rhythm"]),
                }
                for i in range(iteration_range + 1)
                # filter out only dates in time range given in function call
                if event_datetime_start + timedelta(days=i * event_item["rhythm"])
                >= datetime_range_from
            ]
            event_list.append(date_list.copy())
        else:
            date_list = [
                {
                    "name": event_item["name"],
                    "from": event_datetime_start,
                    "to": event_datetime_end,
                }
                for i in range(1)
                if event_datetime_start >= datetime_range_from
            ]

    return event_list


def test():
    # print(data)
    data = load_config("event_config.json")
    dt1 = datetime(2020, 4, 1)
    dt2 = datetime(2020, 4, 30)
    event_list = calc_dates_from_event(data, dt1, dt2)
    # print(event_list)


if __name__ == "__main__":
    test()
