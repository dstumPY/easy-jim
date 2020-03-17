import typing
import locale
from holidays import Germany
from dates_scraping import read_datetimes_from_csv
from dates_calcualtion import load_config, calc_dates_from_event
from datetime import date, time, datetime, timedelta

locale.setlocale(locale.LC_ALL, "de_DE.utf8")

EVENT_CONFIG_PATH = "event_config.json"
SCRAPED_DATES_PATH = "results.csv"
DATES_FROM = date(2020, 4, 1)
DATES_TO = date(2020, 4, 30)

MONTH_DICT = {
    "January": "Januar",
    "February": "Februar",
    "March": "März",
    "April": "April",
    "May": "Mai",
    "June": "Juni",
    "July": "Juli",
    "August": "August",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Dezember",
}

DAY_DICT = {
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Sunday": "Sonntag",
}


def get_holidays(
    prov: str = "NW", year: int = datetime.now().year
) -> typing.List[datetime.date]:

    # create holiday
    holiday_dict = Germany(prov=prov, years=year)
    # extract only key dates
    result_list = list(holiday_dict.keys())
    # add an an extra date
    result_list.append(datetime(year, 12, 27).date())
    result_list.append(datetime(year, 12, 28).date())
    result_list.append(datetime(year, 12, 29).date())
    result_list.append(datetime(year, 12, 30).date())
    result_list.append(datetime(year, 12, 31).date())

    return result_list


def sort_part_list(
    # filter_item: datetime,
    dict_list: typing.List[typing.Dict[str, datetime]]
) -> typing.List[typing.Dict[str, datetime]]:

    # sort list first by "from"-key in dict-list
    first_sort = sorted(dict_list, key=lambda key: key["from"])

    # get set with unique "from" values to iterate throught it afterwards
    unique_list = set(dt_item["from"] for dt_item in first_sort)
    # sort unique list again
    unique_list = sorted(unique_item for unique_item in unique_list)

    # put
    result_list = []
    for unique_dt in unique_list:
        # initialize list to store temporaty
        tmp_list = []

        # filter list on unique datetime items
        tmp_list = [dt_item for dt_item in first_sort if dt_item["from"] == unique_dt]
        tmp_list = sorted(tmp_list, key=lambda key: key["to"])

        result_list.append(tmp_list.copy())

    # flat the results
    result_list = [item for sublist in result_list for item in sublist]

    return result_list


def create_html_code(dates_list: typing.List[typing.Dict]) -> str:
    html_event_list = []
    for dict_item in dates_list:
        html_str = f"""<div class="title-wrapper"><strong>{dict_item['from'].strftime("%A, %d. %B")}</strong></div>
<div class="title-wrapper">{dict_item['from'].strftime("%H:%M")}-{dict_item['to'].strftime("%H:%M")}<span class="event-title" style="color: #a32929;">&nbsp;</span></div>
<div class="title-wrapper"><span class="event-title" style="color: #a32929;">&nbsp;{dict_item['name']}</span></div>
<div class="title-wrapper"></div>
"""
        html_event_list.append(html_str.copy())
        print(dict_item)
    return html_event_list


if __name__ == "__main__":

    # load dates from scraping file
    scraped_dates_unfiltered = read_datetimes_from_csv(SCRAPED_DATES_PATH)
    # filter out events inside the required  date range
    scraped_dates = [
        date
        for date in scraped_dates_unfiltered
        if DATES_FROM <= date["from"].date() <= DATES_TO
    ]

    # load event settings from config file
    event_settings = load_config(EVENT_CONFIG_PATH)
    # calculate dates from event settings
    events = calc_dates_from_event(event_settings, DATES_FROM, DATES_TO)
    # flatten
    calculated_dates = [event for sublist in events for event in sublist]

    dates_list = scraped_dates + calculated_dates

    # sort dates by from key first, to key second
    dates_list_sorted = sort_part_list(dates_list)

    htmml_code = create_html_code(dates_list)
    print("bla")

