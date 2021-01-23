from .base import *

ITEM_PIPELINES = {
    "city_scrapers_core.pipelines.DefaultValuesPipeline": 100,
    "pipelines.FileSystemDiffPipeline": 200,
    "city_scrapers_core.pipelines.MeetingPipeline": 300,
    "city_scrapers_core.pipelines.OpenCivicDataPipeline": 400,
}

COMMANDS_MODULE = "commands"

FEED_EXPORTERS = {
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
}

FEED_FORMAT = "jsonlines"

FEED_OUTPUT_DIRECTORY = "output"

FEED_URI = (
    FEED_OUTPUT_DIRECTORY + "/%(year)s/%(month)s/%(day)s/%(hour_min)s/%(name)s.json"
)
