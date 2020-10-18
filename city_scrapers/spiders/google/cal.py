"""A generic spider for the Google Calendar API

See README.md, in this directory, for more details.
"""

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
            api_key: str, 
            calendar_id: str,
            query_params: dict,
            *args, **kwargs):
        """Construct a GoogleCalendarSpider

        Args:
            api_key: A Google API key
            calendar_id: The id of a Google Calendar
            query_params: Parameters to pass to the calendar "list" query, in a dict.
                Example - request all events from (today - 6 months) to (today + 6 months):
                    {
                        "timeZone": "America/New_York",
                        "timeMin": (datetime.utcnow() - timedelta(days=180)).isoformat() + "Z"
                        "timeMax": (datetime.utcnow() + timedelta(days=180)).isoformat() + "Z"
                    }
                    Note that datetime parameters should be UTC, ISO-formatted strings 
                    (we append a Z to indicate UTC time, since python doesn't do that for us).
                See the Google API documentation for a full list of query parameters: 
                https://developers.google.com/calendar/v3/reference/events/list
        """
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.calendar_id = calendar_id
        self.google_service = build('calendar', 'v3', developerKey=self.api_key)
        self.query_params = query_params

    def start_requests(self) -> Request:
        """Initiate requests to the Google Calendar API.

        This overrides scrapy's default `start_requests`. This means that 
        inheritors of this class should not expect the typical scraper setup
        to work (writing a `parse` function and setting `start_urls`). If 
        that's needed, consider basing your spider on `CityScrapersSpider`
        instead.
        """

        # This is a little awkward; we use the google api library to create
        # the request URL, but use Scrapy to actually issue the request. This 
        # seemed like a reasonable compromise; it avoids having to build the
        # request manually. But perhaps we shouldn't be using Scrapy here,
        # at all.
        events_request = self.google_service.events().list(
            calendarId=self.calendar_id,
            pageToken=None,
            **self.query_params)

        # If the request succeeds, the "on_events_received" callback is invoked
        return [Request(url=events_request.uri, callback=self.on_events_received)]

    def on_events_received(self, response: Response):
        """Handle a successful invocation of the Google Calendar API"""
        body = json.loads(response.body)
        events = body.get("items")

        # Turn Google Calendar events into Meeting objects
        for event in events:
            meeting = self.google_calendar_event_to_meeting(event)
            if meeting:
                yield meeting

        # There might be multiple pages of results. We handle that case here,
        # "recursively" invoking this callback until there are no more pages.
        next_page = body.get("nextPageToken")
        if next_page:
            self.logger.info("Processing the next page of Google calendar events.")
            events_request = self.google_service.events().list(
                calendarId=self.calendar_id,
                pageToken=next_page,
                **self.query_params)
            yield Request(url=events_request.uri, callback=self.on_events_received)
        else:
            self.logger.info("No more pages.")

    def google_calendar_event_to_meeting(self, event: dict) -> Optional[Meeting]:
        """Convert a Google Calendar event into a Meeting

        The event is a dictionary obtained from a Google Calendar API response.
        See the following for a description of the fields in this dictionary:
        https://developers.google.com/calendar/v3/reference/events#resource
        """

        # We delegate to other methods to extract the individual fields
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

        # Delegate to the base clas to set status and id
        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)
        return meeting

    def get_title(self, event: dict) -> Optional[str]:
        """Extract a meeting title from a Google Calendar event"""
        return event.get("summary")

    def get_description(self, event: dict) -> Optional[str]:
        """Extract a meeting description from a Google Calendar event"""
        return event.get("description")

    def get_classification(self, event: dict) -> Optional[str]:
        """Extract a meeting classification from a Google Calendar event"""
        # Nothing done at this level; implementers can override if needed
        return NOT_CLASSIFIED

    def google_time_to_meeting_time(self, time_field):
        """Convert a Google Calendar event time to a Meeting-appropriate format"""
        # Note that we remove timezone info (tzinfo=None), since 
        # this seems to be expected by the City Scraper Meeting pipeline
        if time_field:
            if "dateTime" in time_field:
                dt = start.get("dateTime")
                return dateutil.parser.parse(dt).replace(tzinfo=None)
            elif "date" in start:
                date = start.get("date")
                return dateutil.parser.parse(date).replace(tzinfo=None)
        return None

    def get_start(self, event: dict) -> Optional[datetime]:
        """Extract a meeting start time from a Google Calendar event"""
        return self.google_time_to_meeting_time(event.get("start"))

    def get_end(self, event: dict) -> Optional[datetime]:
        """Extract a meeting end time from a Google Calendar event"""
        return self.google_time_to_meeting_time(event.get("end"))
    
    def get_all_day(self, event: dict) -> bool:
        """Determine whether the event is all day"""
        # If the start date is a "date" instead of a datetime, conclude that
        # the meeting is all day.
        start = event.get("start")
        return start and "date" in start and "dateTime" not in start

    def get_time_notes(self, event: dict) -> Optional[str]:
        """Extract meeting time notes from a Google Calendar event"""
        # A no-op; override if needed 
        return None

    def get_location(self, event: dict) -> dict:
        """Extract a meeting location from a Google Calendar event"""
        return {
            "address": event.get("location"),
            "name": ""
        }

    def get_links(self, event: dict) -> list:
        """Extract meeting links from a Google Calendar event"""
        # A no-op; override if needed 
        return []

    def get_source(self, event: dict) -> Optional[str]:
        """Extract a meeting source link from a Google Calendar event"""
        return event.get("htmlLink")
