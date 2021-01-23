"""Import the "combinefeeds" command from the city_scrapers_core project

We make one enhancement to this command: we allow aggregating
spider results in a local directory, instead of requiring
an S3 bucket or Azure blob. This can be useful for local testing.
"""

import json
import os
from datetime import datetime, timedelta
from operator import itemgetter

import city_scrapers_core.commands.combinefeeds as combinefeeds
from scrapy.exceptions import UsageError

import utils


class Command(combinefeeds.Command):
    def run(self, args, opts):
        storages = self.settings.get("FEED_STORAGES", {})
        output_dir = self.settings.get("FEED_OUTPUT_DIRECTORY", None)
        if "s3" in storages:
            self.combine_s3()
        elif "azure" in storages:
            self.combine_azure()
        elif output_dir is not None:
            self.combine_directory(output_dir)
        else:
            raise UsageError(
                "Either 's3' or 'azure' must be in FEED_STORAGES"
                "to combine past feeds, or FEED_OUTPUT_DIRECTORY set."
            )

    def combine_directory(self, root):
        index = utils.build_spider_index(root)
        meetings = []
        for key in index:
            outputs = sorted(index[key])
            if outputs:
                latest = outputs[-1]
                with open(latest) as f:
                    meetings.extend([json.loads(line) for line in f.readlines()])

        meetings = sorted(meetings, key=itemgetter(self.start_key))
        yesterday_iso = (datetime.now() - timedelta(days=1)).isoformat()[:19]
        upcoming = [
            meeting
            for meeting in meetings
            if meeting[self.start_key][:19] > yesterday_iso
        ]

        with open(os.path.join(root, "latest.json"), "w") as f:
            f.write("\n".join([json.dumps(meeting) for meeting in meetings]))
        with open(os.path.join(root, "upcoming.json"), "w") as f:
            f.write("\n".join([json.dumps(meeting) for meeting in upcoming]))
