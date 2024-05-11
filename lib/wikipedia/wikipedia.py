import json

import requests

from lib.wikipedia.models.wikipedia_api_article import WikipediaAPIArticle


class Wikipedia:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/w/api.php"

    def get_articles_by_coordinates(
        self,
        lat: float,
        lon: float,
        meters_max_radius: int = 10000,
        article_limit: int = 100,
    ) -> list[WikipediaAPIArticle]:
        params = {
            "action": "query",
            "format": "json",
            "list": "geosearch",
            "gscoord": f"{lat}|{lon}",
            "gsradius": meters_max_radius,
            "gslimit": article_limit,
        }
        response = requests.get(self.base_url, params=params)
        data = json.loads(response.text)
        articles = [
            WikipediaAPIArticle(
                title=article["title"],
                page_id=article["pageid"],
                lat=article["lat"],
                lon=article["lon"],
                meters_distance=article["dist"],
            )
            for article in data["query"]["geosearch"]
        ]
        return sorted(articles, key=lambda x: x.meters_distance)
