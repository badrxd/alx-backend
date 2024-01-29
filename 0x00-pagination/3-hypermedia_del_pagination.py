#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Optional


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

    def get_hyper_index(self, index: Optional[int] = None,
                        page_size: int = 10) -> Dict:
        """ return """
        ln = len(self.__indexed_dataset)
        assert index is None or (type(index) is int and 0 <= index < ln)
        assert type(page_size) is int and page_size > 0
        if index is None:
            return {}
        current_index = index
        arr: List = []
        i = current_index
        while len(arr) < page_size:
            if i in self.__indexed_dataset:
                arr.append(self.__indexed_dataset[i])
            i += 1
        return {
            'index': current_index,
            'data': arr,
            'page_size': page_size,
            'next_index': i
        }
