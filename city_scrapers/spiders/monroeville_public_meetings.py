"""A Google Calendar spider for Monroevile public meetings

This spider scrapers the Google Calendar provided by the 
Municipality of Monroeville at this link:
    https://www.monroeville.pa.us/calendar.htm

The ID for this calendar, determined by inspecting
network requests is:
    municipalityofmonroeville@gmail.com

To use this spider, a Google API key must be stored in the
environment variable, "GOOGLE_API_KEY", e.g.

export GOOGLE_API_KEY=your_api_key
scrapy crawl monroeville_public_meetings
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from city_scrapers_core.items import Meeting
from city_scrapers.spiders.google.cal import GoogleCalendarSpider

import scrapy
import dateutil


class MonroevillePublicMeetings(GoogleCalendarSpider):
    name = "monroeville_public_meetings"
    agency = "Municipality of Monroeville"
    timezone = "America/New_York"
    CALENDAR_ID = "municipalityofmonroeville@gmail.com"

    def __init__(self, google_api_key=None, *args, **kwargs):
        time_min = (datetime.utcnow() - timedelta(days=180)).isoformat() + "Z"
        time_max = (datetime.utcnow() + timedelta(days=180)).isoformat() + "Z"

        if google_api_key is None:
            if "GOOGLE_API_KEY" not in os.environ:
                raise RuntimeError(
                    "This spider requires a Google API key to be stored "
                    "in the environment variable 'GOOGLE_API_KEY'"
                )
            google_api_key = os.environ["GOOGLE_API_KEY"]

        request_params = {
            "singleEvents": True,
            "timeZone": self.timezone,
            "maxAttendees": 1,
            "timeMin": time_min,
            "timeMax": time_max,
        }
        super().__init__(
            google_api_key, self.CALENDAR_ID, request_params, *args, **kwargs
        )
