#!/usr/bin/env python3
"""Simple helper function"""
from typing import Tuple, List
import csv
import math


def index_range(page: int, page_size: int) -> Tuple:
    """function return a tuple of size two containing
    a start index and an end index
    """
    return ((page-1)*page_size, page*page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """return """
        assert type(page) is int
        assert page > 0
        assert type(page_size) is int
        assert page_size > 0
        data = self.dataset()

        if page == 1:
            start = page-1
            end = start + page_size
        else:
            start = page
            end = start + page_size+1

        if end > len(data) - 1:
            return []
        return data[start:end]
