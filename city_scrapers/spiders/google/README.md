# Google Spiders

## Google Calendar API Spider

The `GoogleCalendarSpider` class in [cal.py](cal.py) implements a
generic spider for extracting meetings from a Google Calendar.
This isn't a "spider" in the traditional sense: it doesn't scrape an 
html webpage, for example. Instead, it interacts with the Google 
Calendar API, specifically the "list" endpoint described here:
- https://developers.google.com/calendar/v3/reference/events/list

Scrapy might not be ideal tool for this job; it might be easier, for example,
to just use the Google API python library directly. But this approach
integrates cleanly into typical City Scraper spider development flow.

### Using this spider
To write a spider based on this class, first create a new class which 
inherits from `GoogleCalendarSpider`. Then, write an `__init__` method 
as follows:

```
class MyGoogleCalendarSpider(GoogleCalendarSpider):
    name = "scraper_name
    agency = "Agency Name"
    timezone = "Meeting Timezone"

    def __init__(self, *args, **kwargs):
        super().__init__(
            "YOUR_GOOGLE_API_KEY_HERE",
            "YOUR_CALENDAR_ID_HERE",
            # Query parameters here 
            {
               "timeZone": self.timezone,
               "timeMin": (datetime.utcnow() - timedelta(days=180)).isoformat() + "Z"
               "timeMax": (datetime.utcnow() + timedelta(days=180)).isoformat() + "Z"
            },
            *args, 
            **kwargs)
```

This should be enough for a basic implementation. If you find that the base
class isn't translating events to `Meeting` objects correctly, you can override
the various `get_*` methods, e.g. `get_start` and/or `get_location`. You 
can also override `google_calendar_event_to_meeting` to have complete
control over how Meeting objects are derived from Google Calendar events.
