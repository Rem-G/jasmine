class Tweet_service:
    def __init__(self, tweets) -> None:
        self.tweets = tweets
        self.hashtag = self.find_hastag()

    def find_hastag(self) -> list:
        hashtag = []
        worlds = self.tweets.split(" ")
        for world in worlds:
            if world[0] == "#":
                hashtag.append(world)
        return hashtag 