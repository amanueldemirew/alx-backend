#!/usr/bin/env python3
"""
Helper function
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """
    Calculates the start and end index of a range of indexes to return in a
    list based on the given page number and page size.
    """
    start = (page - 1) * page_size
    end = start + page_size

    return start, end
