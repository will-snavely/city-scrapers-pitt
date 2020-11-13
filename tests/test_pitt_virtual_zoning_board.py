from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_virtual_zoning_board import PittVirtualZoningBoardSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_virtual_zoning_board.html"),
    url="https://pittsburghpa.gov/dcp/virtual-zba",
)
spider = PittVirtualZoningBoardSpider()

freezer = freeze_time("2020-10-21")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert (
        parsed_items[0]["title"]
        == "City of Pittsburgh Virtual Zoning Board of Adjustments Meeting"
    )


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 11, 5, 9, 0)


def test_end():
    assert parsed_items[0]["end"] == None


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Please double-check https://pittsburghpa.gov/dcp/virtual-zba to confirm the start time."
    )


def test_id():
    assert (
        parsed_items[0]["id"]
        == "pitt_virtual_zoning_board/202011050900/x/city_of_pittsburgh_virtual_zoning_board_of_adjustments_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "200 Ross St., 3rd Floor, Pittsburgh, PA 15219",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://pittsburghpa.gov/dcp/virtual-zba"


def test_links():
    assert parsed_items[0]["links"] == []


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


def test_all_day():
    assert parsed_items[0]["all_day"] is False
