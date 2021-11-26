
from service.client_twitter import Client

class Hashtag_finder():
    entry_points = [] # Base Hashtag for start the reasearch
    def __init__(self, entry_points, date_start, date_end) -> None:
        self.entry_points = entry_points
        self.date_start = date_start
        self.date_end = date_end