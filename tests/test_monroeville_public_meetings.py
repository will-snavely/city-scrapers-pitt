from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.monroeville_public_meetings import MonroevillePublicMeetings

test_response = file_response(
    join(dirname(__file__), "files", "monroevile_public_meetings.json"),
    url="https://www.googleapis.com/calendar/v3/calendars/",
)
spider = MonroevillePublicMeetings()

freezer = freeze_time("2020-10-18")
freezer.start()

parsed_items = [
    item for item in spider.on_events_received(test_response, fetch_next=False)
]
freezer.stop()


def test_title():
    expected_titles = ["Planning Commission Work Session"] * 5
    actual_titles = [meeting["title"] for meeting in parsed_items]
    assert expected_titles == actual_titles


def test_start():
    expected_start_dates = {
        datetime(year=2020, month=5, day=20, hour=19, minute=0),
        datetime(year=2020, month=6, day=17, hour=19, minute=0),
        datetime(year=2020, month=7, day=15, hour=19, minute=0),
        datetime(year=2020, month=8, day=19, hour=19, minute=0),
        datetime(year=2020, month=10, day=21, hour=19, minute=0),
    }

    actual_start_dates = {meeting["start"] for meeting in parsed_items}

    assert expected_start_dates == actual_start_dates


def test_end():
    expected_end_dates = {
        datetime(year=2020, month=5, day=20, hour=20, minute=30),
        datetime(year=2020, month=6, day=17, hour=20, minute=30),
        datetime(year=2020, month=7, day=15, hour=20, minute=30),
        datetime(year=2020, month=8, day=19, hour=20, minute=30),
        datetime(year=2020, month=10, day=21, hour=20, minute=30),
    }

    actual_end_dates = {meeting["end"] for meeting in parsed_items}
    assert expected_end_dates == actual_end_dates


def test_time_notes():
    for item in parsed_items:
        assert item["time_notes"] == ""


def test_location():
    expected_locations = ["2700 Monroeville Blvd. Monroeville, PA 15146"] * 5

    idx = 0
    for item in parsed_items:
        assert item["location"]["address"] == expected_locations[idx]
        assert item["location"]["name"] == ""
        idx += 1


def test_classification():
    for item in parsed_items:
        assert item["classification"] == NOT_CLASSIFIED


def test_all_day():
    for item in parsed_items:
        assert item["all_day"] is False


def test_meeting_ids():
    for item in parsed_items:
        assert item["id"] is not None
