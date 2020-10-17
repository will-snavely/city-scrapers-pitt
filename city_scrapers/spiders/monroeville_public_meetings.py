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

    def __init__(self, *args, **kwargs):
        time_min = (datetime.utcnow() - timedelta(days=180)).isoformat() + "Z"
        time_max = (datetime.utcnow() + timedelta(days=180)).isoformat() + "Z"
        google_api_key = os.environ["GOOGLE_API_KEY"] 
        request_params = {
            "singleEvents": True,
            "timeZone": self.timezone,
            "maxAttendees": 1,
            "timeMin": time_min,
            "timeMax": time_max,
        }
        super().__init__(
                google_api_key,
                self.CALENDAR_ID,
                request_params,
                *args, 
                **kwargs)
