import json
from typing import List

import requests

from lib.wikipedia.models.wikipedia_api_article import WikipediaAPIArticle
from lib.wikipedia.models.wikipedia_article import (
    WikipediaArticle,
    WikipediaArticleFullText,
)


class Wikipedia:

    BASE_URL = "https://en.wikipedia.org/w/api.php"

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
        response = requests.get(self.BASE_URL, params=params)
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

    def get_article_summary_from_page_id(self, page_id: int) -> WikipediaArticle:
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "pageids": page_id,
            "explaintext": True,
            "exintro": True,
        }
        response = requests.get(self.BASE_URL, params=params)
        data = json.loads(response.text)
        return WikipediaArticle(
            title=data["query"]["pages"][str(page_id)]["title"],
            page_id=page_id,
            summary=self._parse_wikipedia_text(
                data["query"]["pages"][str(page_id)]["extract"]
            ),
            categories=self.get_article_categories_from_page_id(page_id),
        )

    def get_article_categories_from_page_id(self, page_id: int) -> List[str]:
        params = {
            "action": "query",
            "format": "json",
            "prop": "categories",
            "pageids": page_id,
            "cllimit": "30",
        }
        response = requests.get(self.BASE_URL, params=params)
        data = json.loads(response.text)
        return [
            category["title"].split(":")[1]
            for category in data["query"]["pages"][str(page_id)]["categories"]
        ]

    def get_full_article_from_wikipedia_article(
        self, article: WikipediaArticle
    ) -> WikipediaArticle:
        page_id = article.page_id
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "pageids": page_id,
            "explaintext": True,
        }
        response = requests.get(self.BASE_URL, params=params)
        data = json.loads(response.text)
        return WikipediaArticleFullText(
            title=article.title,
            page_id=page_id,
            summary=article.summary,
            full_text=self._parse_wikipedia_text(
                data["query"]["pages"][str(page_id)]["extract"]
            ),
        )

    @staticmethod
    def _parse_wikipedia_text(text: str) -> str:
        return text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
