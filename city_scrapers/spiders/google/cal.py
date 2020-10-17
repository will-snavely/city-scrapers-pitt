import json
import logging
from datetime import datetime
from typing import Optional

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

import dateutil
from scrapy.http import Request, Response
from googleapiclient.discovery import build

class GoogleCalendarSpider(CityScrapersSpider):
    def __init__(
            self,
            api_key, 
            calendar_id,
            request_params,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.calendar_id = calendar_id
        self.google_service = build('calendar', 'v3', developerKey=self.api_key)
        self.request_params = request_params

    def start_requests(self) -> Request:
        events_request = self.google_service.events().list(
            calendarId=self.calendar_id,
            pageToken=None,
            **self.request_params)
        return [Request(url=events_request.uri, callback=self.on_events_received)]

    def get_title(self, event: dict) -> Optional[str]:
        return event.get("summary")

    def get_description(self, event: dict) -> Optional[str]:
        return event.get("description")

    def get_classification(self, event: dict) -> Optional[str]:
        return NOT_CLASSIFIED

    def get_start(self, event: dict) -> Optional[datetime]:
        start = event.get("start")
        if start:
            if "dateTime" in start:
                start_datetime = start.get("dateTime")
                return dateutil.parser.parse(start_datetime).replace(tzinfo=None)
            elif "date" in start:
                start_date = start.get("date")
                return dateutil.parser.parse(start_date).replace(tzinfo=None)
        return None

    def get_end(self, event: dict) -> Optional[datetime]:
        end = event.get("end")
        if end:
            end_datetime = end.get("dateTime")
            try:
                return dateutil.parser.parse(end_datetime).replace(tzinfo=None)
            except:
                pass
        return None
    
    def get_all_day(self, event: dict) -> bool:
        start = event.get("start")
        return start and "date" in start and "dateTime" not in start

    def get_time_notes(self, event: dict) -> Optional[str]:
        return None

    def get_location(self, event: dict) -> dict:
        return {
            "address": event.get("location"),
            "name": ""
        }

    def get_links(self, event: dict) -> list:
        return []

    def get_source(self, event: dict) -> Optional[str]:
        return event.get("htmlLink")

    def google_calendar_event_to_meeting(self, event: dict) -> Optional[Meeting]:
        meeting = Meeting(
            title=self.get_title(event) or "",
            description=self.get_description(event) or "",
            classification=self.get_classification(event),
            start=self.get_start(event),
            end=self.get_end(event),
            all_day=self.get_all_day(event),
            time_notes=self.get_time_notes(event),
            location=self.get_location(event),
            links=self.get_links(event),
            source=self.get_source(event),
        )

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)
        return meeting

    def on_events_received(self, response: Response):
        body = json.loads(response.body)
        events = body.get("items")
        for event in events:
            meeting = self.google_calendar_event_to_meeting(event)
            if meeting:
                yield meeting

        next_page = body.get("nextPageToken")
        if next_page:
            self.logger.info("Processing the next page of Google calendar events.")
            events_request = self.google_service.events().list(
                calendarId=self.calendar_id,
                pageToken=next_page,
                **self.request_params)
            yield Request(url=events_request.uri, callback=self.on_events_received)
        else:
            self.logger.info("No more pages.")

