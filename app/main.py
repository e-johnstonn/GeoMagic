from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from lib.geocode.geocoder import Geocoder
from lib.wikipedia.models.wikipedia_article import WikipediaArticle
from lib.wikipedia.wikipedia import Wikipedia

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/closest-article", response_model=WikipediaArticle)
async def closest_article(location: str) -> WikipediaArticle:
    try:
        geocoded = Geocoder().geocode_from_address(location)
        wikipedia = Wikipedia()
        articles = wikipedia.get_articles_by_coordinates(
            geocoded.latitude, geocoded.longitude
        )
        closest_article = articles[0]
        article_summary = wikipedia.get_article_summary_from_page_id(
            closest_article.page_id
        )
        return article_summary
    except Exception:
        raise HTTPException(status_code=500, detail="Error handling? What's that?")
