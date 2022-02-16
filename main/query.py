import logging
from typing import Optional, List

from main.influence import Influence
from stubs.pathspec import PathSpec
from stubs.time import Time


class Query:
    def __init__(self, influences: List[Influence], time: Optional[Time] = None, path: Optional[PathSpec] = None):
        self.logger = logging.getLogger(__name__)
        self.influences: List[Influence] = influences
        self.time: Optional[Time] = time
        self.path: Optional[PathSpec] = path
