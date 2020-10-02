from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from dateutil import tz
from freezegun import freeze_time

from city_scrapers.spiders.bethel_park_public_meetings import BethelParkSpider

test_response = file_response(
    join(dirname(__file__), "files", "bethel_park", "bethel_park_public_meetings.ics"),
    url="http://bethelpark.net/?"
    "plugin=all-in-one-event-calendar"
    "&controller=ai1ec_exporter_controller"
    "&action=export_events"
    "&ai1ec_cat_ids=42"
    "&no_html=true",
)
spider = BethelParkSpider()

freezer = freeze_time("2020-08-23")
freezer.start()
parsed_items = [item for item in spider.parse(test_response)]
freezer.stop()


def get_test_sample():
    """Return a sample of meetings from the scraped calendar.

    Currently, we return the six latest meetings.
    """
    return sorted(parsed_items, key=lambda e: e["start"], reverse=True)[:6]


def test_event_count():
    assert len(parsed_items) == 28


def test_titles():
    expected_titles = [
        "Council Committee Meeting",
        "Shade Tree Commission Meeting",
        "Shade Tree Commission Meeting",
        "Zoning Hearing Board",
        "Planning & Zoning Commission Workshop Meeting",
        (
            "Municipal Council Committee Meeting July 27th, 2020 7:30 PM "
            "– Public Hearings starting at 6:30 PM"
        ),
    ]
    for (event, expected_title) in zip(get_test_sample(), expected_titles):
        assert event["title"] == expected_title


def test_start():
    tzinfo = tz.gettz("America/New_York")
    expected_start_dates = [
        datetime(year=2021, month=1, day=27, hour=19, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=11, day=18, hour=18, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=9, day=16, hour=18, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=9, day=8, hour=19, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=7, day=29, hour=19, minute=00, tzinfo=tzinfo),
        datetime(year=2020, month=7, day=27, hour=18, minute=30, tzinfo=tzinfo),
    ]
    for (event, expected_start) in zip(get_test_sample(), expected_start_dates):
        assert event["start"].year == expected_start.year
        assert event["start"].month == expected_start.month
        assert event["start"].day == expected_start.day
        assert event["start"].hour == expected_start.hour
        assert event["start"].minute == expected_start.minute
        assert event["start"].tzname() == expected_start.tzname()


def test_end():
    # The reason the first five end dates are None: the source returns these events
    # with an end time equal to the start time. In this case, the spider sets "None"
    # for the end time so that the scrapy pipeline can fill it a default. Only the
    # six event has a different end date set, in this specific data set.
    tzinfo = tz.gettz("America/New_York")
    expected_end_dates = [
        None,
        None,
        None,
        None,
        None,
        datetime(year=2020, month=7, day=27, hour=21, minute=00, tzinfo=tzinfo),
    ]
    for (event, expected_end) in zip(get_test_sample(), expected_end_dates):
        if expected_end is None:
            assert event["end"] is None
        else:
            assert event["end"].year == expected_end.year
            assert event["end"].month == expected_end.month
            assert event["end"].day == expected_end.day
            assert event["end"].hour == expected_end.hour
            assert event["end"].minute == expected_end.minute
            assert event["end"].tzname() == expected_end.tzname()


def test_location():
    expected_locations = [
        "Council Caucus Room @ 5100 West Library Ave. Bethel Park, PA 15102",
        (
            "Municipal Building Council Chambers "
            "@ 5100 West Library Ave Bethel Park, PA 15102"
        ),
        # Note there are slight variations in how the locations are reported,
        # e.g. missing a comma in this case
        "Municipal Building Council Chambers @ 5100 West Library Ave Bethel Park PA 15102",
        "5100 West Library Ave. Bethel Park, PA 15102 @ Council Chambers",
        "5100 West Library Ave. Bethel Park, PA 15102 @ Council Chambers",
        "Municipal Building Council Chambers @ 5100 West Library Road",
    ]
    for (event, expected_location) in zip(get_test_sample(), expected_locations):
        assert event["location"] == expected_location


def test_classification():
    # The events returned by the Bethel Park site don't expose a consistent
    # category/classification; everything is kind of lumped together. For
    # now, therefore, classification is uniformly set to "NOT_CLASSIFIED
    for item in parsed_items:
        assert item["classification"] == NOT_CLASSIFIED


def test_all_day():
    # The icalendar events don't expose an "all day" flag. They only have a start and end time.
    for item in parsed_items:
        assert item["all_day"] is False


def test_description():
    with open(join(dirname(__file__), "files", "bethel_park", "long_description")) as f:
        long_description = f.read()

    expected_descriptions = [
        # Some meetings are missing a description
        None,
        None,
        None,
        None,
        "Meeting Agenda",
        # This meeting has a very length description that we store in a file to keep this
        # test class a little neater
        long_description,
    ]
    for (event, expected_description) in zip(get_test_sample(), expected_descriptions):
        assert event["description"] == expected_description
