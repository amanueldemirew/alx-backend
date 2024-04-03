#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Method to get a hypermedia page based on index
        """
        assert isinstance(index,
                          (int, type(None))) and (index is None or index >= 0)
        assert isinstance(page_size, int) and page_size > 0

        indexed_dataset = self.indexed_dataset()

        if index is None:
            index = 0

        if index >= len(indexed_dataset):
            return {}

        start = index
        end = start + page_size

        # Check if some rows were deleted from the dataset
        while end < len(indexed_dataset) and indexed_dataset.get(end) is None:
            end += 1

        # If the last page contains deleted rows, adjust the page size
        if end >= len(indexed_dataset) and indexed_dataset.get(start) is None:
            page_size = end - start

        data = [indexed_dataset[i]
                for i in range(start, end)
                if indexed_dataset.get(i) is not None]

        return {
            "index": start,
            "data": data,
            "page_size": page_size,
            "next_index": end if end < len(indexed_dataset) else None
        }
