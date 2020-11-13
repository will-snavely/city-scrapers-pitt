from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pa_utility import PaUtilitySpider

test_response = file_response(
    join(dirname(__file__), "files", "pa_utility.html"),
    url="https://www.puc.pa.gov/about-the-puc/public-meetings-hearings/?MeetingType=meeting&MeetingBeginDate=2016-01-01&MeetingEndDate=2050-01-01&ufprt=69EB449024234D5997764DC69DFD1A21801B2873C28077463921ED5CEF44E9B8B794979267EF2FC3425F687CF2D3838EA24F9237B87364F056725A1384E44CD3A62CFFB5CA2503A0AE3B12AF0558F3BE09D1E2A5E3FE38D4B8044520CA32607246EE4A0D33DEF6F5C06714AF80E97E6F4A8592C0FB57E42B7056340C5A8350B140C1D0E93CA34DCE5886BC4B72C32A88226777E168FC024AA9CCCCFEDCA4FAB0203DDF37AFAF1442D15EFA91D4D5E8A21E3052D0A4C1328F6F3F9D221E3B0BB065370894AABC094C0CB0301D1C49CE79BE645BAA74FAFD36A0CF2AF1634ECA269471CD417AC5BFBA803E623AC8A17C6D#search-results",
)
spider = PaUtilitySpider()

freezer = freeze_time("2020-10-21")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[8]["title"] == "PA Public Utility Commission Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2021, 6, 17, 10, 0)


def test_end():
    assert parsed_items[0]["end"] == None


def test_time_notes():
    assert (
        parsed_items[18]["time_notes"]
        == "Please double-check https://www.puc.pa.gov to confirm the start time.\nRescheduled from June 11, 2020."
    )
    assert (
        parsed_items[10]["time_notes"]
        == "Please double-check https://www.puc.pa.gov to confirm the start time."
    )


def test_id():
    assert (
        parsed_items[0]["id"]
        == "pa_utility/202106171000/x/pa_public_utility_commission_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"
    assert parsed_items[18]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Commonwealth Keystone Building",
        "address": "Room No. 1, 400 North St, Harrisburg, PA 17120",
    }


def test_source():
    href = "https://www.puc.pa.gov/about-the-puc/public-meetings-hearings/?MeetingType=meeting&MeetingBeginDate=2016-01-01&MeetingEndDate=2050-01-01&ufprt=69EB449024234D5997764DC69DFD1A21801B2873C28077463921ED5CEF44E9B8B794979267EF2FC3425F687CF2D3838EA24F9237B87364F056725A1384E44CD3A62CFFB5CA2503A0AE3B12AF0558F3BE09D1E2A5E3FE38D4B8044520CA32607246EE4A0D33DEF6F5C06714AF80E97E6F4A8592C0FB57E42B7056340C5A8350B140C1D0E93CA34DCE5886BC4B72C32A88226777E168FC024AA9CCCCFEDCA4FAB0203DDF37AFAF1442D15EFA91D4D5E8A21E3052D0A4C1328F6F3F9D221E3B0BB065370894AABC094C0CB0301D1C49CE79BE645BAA74FAFD36A0CF2AF1634ECA269471CD417AC5BFBA803E623AC8A17C6D"
    assert href in parsed_items[0]["source"]


def test_links():
    assert parsed_items[0]["links"] == [{"href": "", "title": ""}]
    assert parsed_items[18]["links"] == [
        {
            "href": "https://www.puc.pa.gov/documents/public-meeting/800/pm061820.pdf",
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


def test_all_day():
    assert parsed_items[0]["all_day"] == False
