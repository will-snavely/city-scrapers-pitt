from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.jail_oversight import JailOversightSpider

test_response = file_response(
    join(dirname(__file__), "files", "jail_oversight.html"),
    url="https://alleghenycontroller.com/jailoversight/",
)
spider = JailOversightSpider()

freezer = freeze_time("2020-08-07")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


"""
Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"] == "Jail Oversight Board Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 1, 2, 16, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "The Gold Room in the Allegheny County Courthouse on the 4th floor",
        "address": "436 Grant Street, Pittsburgh, PA 15219",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://alleghenycontroller.com/jailoversight/"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.alleghenycourts.us/jail/Oversight.aspx",
            "title": "Oversight Board Meeting",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
