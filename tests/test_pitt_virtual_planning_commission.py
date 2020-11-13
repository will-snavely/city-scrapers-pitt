from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_virtual_planning_commission import (
    PittVirtualPlanningCommissionSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "pitt_virtual_planning_commission.html"),
    url="https://pittsburghpa.gov/dcp/virtual-pc",
)
spider = PittVirtualPlanningCommissionSpider()

freezer = freeze_time("2020-10-20")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert (
        parsed_items[0]["title"]
        == "City of Pittsburgh Virtual Planning Commission Meeting"
    )


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 10, 13, 13, 0)


def test_end():
    assert parsed_items[0]["end"] == None


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Please double-check https://pittsburghpa.gov/dcp/virtual-pc to confirm the start time."
    )


def test_id():
    assert (
        parsed_items[0]["id"]
        == "pitt_virtual_planning_commission/202010131300/x/city_of_pittsburgh_virtual_planning_commission_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "200 Ross St., 4th Floor, Pittsburgh, PA 15219",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://pittsburghpa.gov/dcp/virtual-pc"


def test_links():
    assert parsed_items[0]["links"] == []


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


def test_all_day():
    assert parsed_items[0]["all_day"] is False
