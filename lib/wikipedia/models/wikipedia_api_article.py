from typing import Dict, List

from pydantic import BaseModel


class WikipediaAPIArticle(BaseModel):
    title: str
    page_id: int
    lat: float
    lon: float
    meters_distance: float
