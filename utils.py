import collections
import os
from typing import Mapping


def build_spider_index(root_dir: str) -> Mapping:
    """Build a index of spider results in a directory

    This walks the given directory, finding all spider results, and
    returns a dict mapping spider name to a list of paths
    discovered for that spider.
    """
    result = collections.defaultdict(list)
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for name in files:
            if name.endswith(".json"):
                spider = name.replace(".json", "")
                result[spider].append(os.path.join(root, name))
    return result
