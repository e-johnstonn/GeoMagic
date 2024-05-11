from typing import Optional

from pydantic import BaseModel


class WikipediaArticle(BaseModel):
    title: str
    page_id: int
    summary: str


class WikipediaArticleFullText(WikipediaArticle):
    full_text: str
