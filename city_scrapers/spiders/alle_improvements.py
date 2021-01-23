from datetime import datetime  # convert utc time to datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

from city_scrapers.common.cleaners import scrub_html


class AlleImprovementsSpider(CityScrapersSpider):
    name = "alle_improvements"
    agency = "Allegheny County Authority for Improvements in Municipalities (AIM)"
    timezone = "America/New_York"
    start_urls = [
        (
            "https://www.alleghenycounty.us/economic-development/"
            "authorities/meetings-reports/aim/meetings.aspx"
        ),
    ]

    def parse(self, response) -> Meeting:
        self._check_starting_hour_has_not_changed(response)
        meeting_dates: list = self._parse_meeting_dates_list(response)

        for item in meeting_dates:
            meeting = Meeting(
                title=self._parse_title(),
                description=self._parse_description(),
                classification=self._parse_classification(),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_meeting_dates_list(self, response) -> list:
        root: str = '//*[@id="mainContainer"]/div[3]/section/div[1]/div[2]'
        path: str = root + "/div/div/div/div/div/table/tbody/tr/td[2]/p"
        dates_list: list = response.xpath(path)[0].get().split("<br>")
        dates_list = list(map(scrub_html, dates_list))
        return dates_list

    def _parse_title(self) -> str:
        return f"{self.agency} Board Meeting"

    def _parse_description(self) -> str:
        return ""

    def _parse_classification(self) -> str:
        return BOARD

    def _check_starting_hour_has_not_changed(self, response):
        expected: str = "All meetings start at 9:30 am"
        root: str = '//*[@id="mainContainer"]/div[3]/section/div[1]/div[2]/'
        path: str = root + "div/div/div/div/div/table/tbody/tr/td[1]/p[2]/text()"
        assert response.xpath(path).get() == expected

    def _parse_start(self, item) -> datetime:
        date: datetime = datetime.strptime(item, "%B %d, %Y")
        # Every meeting is assumed to take place at 9:30am
        # as asserted by _check_starting_hour_has_not_changed
        date_with_time_of_day: datetime = date.replace(hour=9, minute=30)
        return date_with_time_of_day

    def _parse_end(self, item) -> datetime:
        return None

    def _parse_time_notes(self, item) -> str:
        return ""

    def _parse_all_day(self, item) -> bool:
        return False

    def _parse_location(self, item) -> dict:
        return {
            "address": "One Chatham Center, Suite 900, 112 Washington Place, Pittsburgh, PA 15219",
            "name": "Chatham Center",
        }

    def _parse_links(self, item) -> list:
        """Parse or generate links."""
        # TODO This would be a "nice to have" but is not necessary right now.
        return [{"href": "", "title": ""}]

    def _parse_source(self, response) -> str:
        """Parse or generate source."""
        return response.url
