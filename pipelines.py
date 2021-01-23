"""A pipeline for diffing newly scraped meetings with
previously scraped meetings, using the file system
as a backing store

This is based on the DiffPipeline element defined in city_scraper_core:
https://github.com/City-Bureau/city-scrapers-core/blob/main/city_scrapers_core/pipelines/diff.py

The purpose of the DiffPipeline is to avoid loading duplicate meeting
entries. However, the city_scraper_core implementations only work
with s3 and azure storage. This implementation works with a local
folder on disk, for testing purposes.
"""

import json
from typing import List, Mapping

from city_scrapers_core.pipelines import DiffPipeline
from pytz import timezone
from scrapy.crawler import Crawler
from scrapy import signals

import utils


class FileSystemDiffPipeline(DiffPipeline):
    def __init__(self, crawler: Crawler, output_format: str):
        """Initialize FileSystemDiffPipeline
        Params:
            crawler: Current Crawler object
            output_format: Currently only "ocd" is supported
        """
        super().__init__(crawler, output_format)
        feed_uri = crawler.settings.get("FEED_URI")
        self.folder = crawler.settings.get("FEED_OUTPUT_DIRECTORY")
        self.spider = crawler.spider
        self.feed_prefix = crawler.settings.get(
            "CITY_SCRAPERS_DIFF_FEED_PREFIX", "%Y/%m/%d"
        )
        self.index = utils.build_spider_index(self.folder)

    def load_previous_results(self) -> List[Mapping]:
        """Walk the local directory, returning the latest result for each spider.
        """
        if self.spider is None:
            return

        tz = timezone(self.spider.timezone)

        # Since the file structure is Year/Month/Day/Time/<spider>.json, sorting
        # should be sufficient to find the most recent spider result
        spider_outputs = sorted(self.index[self.spider.name])
        if len(spider_outputs) > 0:
            latest = spider_outputs[-1]
            with open(latest) as f:
                return [json.loads(line) for line in f.readlines()]
        return []

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """Classmethod for creating a pipeline object from a Crawler

        :param crawler: Crawler currently being run
        :raises ValueError: Raises an error if an output format is not supplied
        :return: Instance of DiffPipeline
        """
        pipelines = crawler.settings.get("ITEM_PIPELINES", {})
        if "city_scrapers_core.pipelines.OpenCivicDataPipeline" in pipelines:
            output_format = "ocd"
        else:
            raise ValueError(
                "An output format pipeline must be enabled for diff middleware"
            )
        pipeline = cls(crawler, output_format)
        if crawler.spider is None:
            return pipeline
        crawler.spider._previous_results = pipeline.load_previous_results()
        if output_format == "ocd":
            crawler.spider._previous_map = {}
            for result in crawler.spider._previous_results:
                extras_dict = result.get("extras") or result.get("extra") or {}
                previous_id = extras_dict.get("cityscrapers.org/id")
                crawler.spider._previous_map[previous_id] = result["_id"]
        crawler.spider._scraped_ids = set()
        crawler.signals.connect(pipeline.spider_idle, signal=signals.spider_idle)
        return pipeline
