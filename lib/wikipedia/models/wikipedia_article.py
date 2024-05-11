from typing import List

from pydantic import BaseModel


class WikipediaArticle(BaseModel):
    title: str
    page_id: int
    summary: str
    categories: List[str] = []


class WikipediaArticleFullText(WikipediaArticle):
    full_text: str
