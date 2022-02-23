import logging
from typing import Optional

from merge.main.influence import Influence
from merge.stubs.pathspec import PathSpec
from merge.stubs.time import Time


class Query:
    def __init__(self, influences: Influence, time: Optional[Time] = None, path: Optional[PathSpec] = None):
        self.logger = logging.getLogger(__name__)
        self.influences: Influence = influences
        self.time: Optional[Time] = time
        self.path: Optional[PathSpec] = path
