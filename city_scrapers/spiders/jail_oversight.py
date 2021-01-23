import re
from datetime import datetime, time

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class JailOversightSpider(CityScrapersSpider):
    name = "jail_oversight"
    agency = "Allegheny County Jail Oversight Board"
    timezone = "America/New_York"
    start_urls = ["https://alleghenycontroller.com/jailoversight/"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for possible_meeting in response.css("div.entry-content p"):
            possible_meeting_date = possible_meeting.re(
                "^<p>(?:<strong>)?([ADFJMNOS][a-z]{2,8} [1-3]?[0-9], [12][0-9]{3})"
            )
            if possible_meeting_date:
                item = possible_meeting_date[0]
                meeting = Meeting(
                    title="Jail Oversight Board Meeting",
                    description="",
                    classification=BOARD,
                    start=self._parse_start(item),
                    end=self._parse_end(item),
                    all_day=False,
                    time_notes="",
                    location=self._parse_location(item),
                    links=self._parse_links(item),
                    source=self._parse_source(response),
                )

                meeting["status"] = self._get_status(meeting)
                meeting["id"] = self._get_id(meeting)

                yield meeting

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        meeting_date = datetime.strptime(item, "%B %d, %Y")
        return datetime.combine(meeting_date, time(16, 0))

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_location(self, item):
        """Parse or generate location."""
        meeting_date = datetime.strptime(item, "%B %d, %Y")
        if meeting_date > datetime(2020, 5, 1):
            return {
                "address": "",
                "name": "Online",
            }
        return {
            "address": "436 Grant Street, Pittsburgh, PA 15219",
            "name": "The Gold Room in the Allegheny County Courthouse on the 4th floor",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "href": "https://www.alleghenycourts.us/jail/Oversight.aspx",
                "title": "Oversight Board Meeting",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
