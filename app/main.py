from fastapi import FastAPI

from lib.geocode.geocoder import Geocoder
from lib.wikipedia.models.wikipedia_article import WikipediaArticle
from lib.wikipedia.wikipedia import Wikipedia

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Howdy, stranger!"}


@app.get("/closest-article", response_model=WikipediaArticle)
async def closest_article(location: str) -> WikipediaArticle:
    geocoded = Geocoder().geocode_from_address(location)
    wikipedia = Wikipedia()
    articles = wikipedia.get_articles_by_coordinates(
        geocoded.latitude, geocoded.longitude
    )
    closest_article = articles[0]
    article_summary = wikipedia.get_article_summary_from_api_article(closest_article)
    return article_summary
