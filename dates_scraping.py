from datetime import date, time, datetime, timedelta
import typing
import csv
import copy
import re


def get_times_from_str(time_range: str) -> (time, time):

    # match strings of form int.int-int.int
    time_split_list = [
        item
        for item in re.split("(\d\d)\.(\d\d)\-(\d\d)\.(\d\d)", time_range)
        if item != ""
    ]

    # extract hours and minutes
    hour_from = int(time_split_list[0])
    minute_from = int(time_split_list[1])
    hour_to = int(time_split_list[2])
    minute_to = int(time_split_list[3])

    # create time objects from list entries
    time_from = time(hour_from, minute_from)
    time_to = time(hour_to, minute_to)

    return time_from, time_to


def read_datetimes_from_csv(path: str):

    datetime_list = []
    # read in csv data
    with open("results.csv", mode="r") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        counter = 0
        for row in reader:
            if counter >= 1:
                # dict to store extracted information
                time_dict = {}
                date_from = datetime.strptime(row["date"], "%d.%m.%Y").date()
                date_to = datetime.strptime(row["date"], "%d.%m.%Y").date()

                # split time range 17.00-18.00 at '-' to 17.00 and 18.00
                assert re.search(
                    "\d\d\.\d\d\-\d\d\.\d\d", row["time"]
                ), f"Input does not match the required scheme. Input was: {row['time']}"
                time_from, time_to = get_times_from_str(row["time"])

                # combine dates and times to datetimes
                time_dict["from"] = datetime.combine(date_from, time_from)
                time_dict["to"] = datetime.combine(date_to, time_to)
                time_dict["name"] = row["name"]
                # store datetime data
                datetime_list.append(time_dict.copy())
            counter += 1
        return datetime_list


# def sort_datetime_list(datetime_list: typing.List[datetime]) -> typing.List[datetime]:
#     first_key_sorted = sorted(datetime_list, key=datetime_list["from"])

#     # get unique first datetime values
#     unique_dts = set([dt["from"] for dt in datetime_list])


# def calc_dates_by_rhythm(
#     start_dt: datetime,
#     end_dt: datetime,
#     rhythm_days: int,
#     last_dt: datetime = datetime(datetime.now().year, 12, 31, 23, 59, 59),
# ) -> typing.List[typing.Dict[str, datetime]]:
#     """ Calculate datetimes by adding a rhythmic amount of days

#     Arguments:
#         start_dt {datetime} -- given start datetiime
#         end_dt {datetime} -- given end datetime
#         rhythm_days {int} -- rhythm in days to be added on start and end datetime

#     Returns:
#         typing.List[typing.Dict[str, datetime]] -- hd = get_holidays()
#     # print(hd)Datetime ranges with rhythm time gap less than last_dt
#     """
#     # rhythm_days == 0 is equal to a single event without repetition
#     if rhythm_days == 0:
#         result_list = [{"from": start_dt, "to": end_dt}]

#     elif rhythm_days > 0:

#         # how many times rhythm_days could be added to start_dt untill last_dt will be exceeded
#         add_days_n_times = int(((last_dt - start_dt).days / rhythm_days))

#         from_list = [
#             start_dt + timedelta(days=i * rhythm_days) for i in range(add_days_n_times)
#         ]
#         to_list = [end_dt + timedelta(i * rhythm_days) for i in range(add_days_n_times)]

#         result_list = [
#             {"from": from_item, "to": to_item}
#             for from_item, to_item in zip(from_list, to_list)
#         ]

#     # Exception for negative rhythm
#     else:
#         raise Exception("The parameter rhythm_days must be non-negetaive.")

#     return result_list


def test():
    # # Test calculatiing the date range

    # # Test case #1
    # dt1 = datetime.now()
    # dt2 = datetime.now() + timedelta(hours = 1)
    # #dt_end = datetime(2020, 12, 31, 23, 59, 59)
    # dt_end = datetime(2020, 12, 31, 23, 59, 59)
    # rhythm = 0
    # test_ls = calc_dates_by_rhythm(dt1, dt2, rhythm, dt_end)
    # print(test_ls)

    # # Test case #2
    # dt1 = datetime.now()
    # dt2 = datetime.now() + timedelta(hours = 1)
    # #dt_end = datetime(2020, 12, 31# Test case #1
    # dt1 = datetime.now()
    # dt2 = datetime.now() + timedelta(hours = 1)
    # #dt_end = datetime(2020, 12, 31, 23, 59, 59)
    # dt_end = datetime(2020, 12, 31, 23, 59, 59)
    # rhythm = 0
    # test_ls = calc_dates_by_rhythm(dt1, dt2, rhythm, dt_end)
    # print(test_ls)

    # # Test case #2
    # dt1 = datetime.now()
    # dt2 = datetime.now() + timedelta(hours = 1)
    # #dt_end = datetime(2020, 12, 31, 23, 59, 59)
    # dt_end = datetime(2020, 12, 31, 23, 59, 59)
    # rhythm = 7
    # test_ls = calc_dates_by_rhythm(dt1, dt2, rhythm, dt_end)
    # print(test_ls), 23, 59, 59)
    # dt_end = datetime(2020, 12, 31, 23, 59, 59)
    # rhythm = 7
    # test_ls = calc_dates_by_rhythm(dt1, dt2, rhythm, dt_end)
    # print(test_ls)

    # #  Test get_holidays
    # hd = get_holidays()
    # print(hd)
    datetime_list = read_datetimes_from_csv("results.csv")
    print(datetime_list)

    # pass


if __name__ == "__main__":

    # full_sorted_list = sort_part_list(datetime_list)
    # print(full_sorted_list)
    test()
