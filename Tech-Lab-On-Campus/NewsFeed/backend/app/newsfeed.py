"""Module for retrieving newsfeed information."""

from dataclasses import dataclass
from datetime import datetime
from app.utils.redis import REDIS_CLIENT


@dataclass
class Article:
    """Dataclass for an article."""

    author: str
    title: str
    body: str
    publish_date: datetime
    image_url: str
    url: str


def _format(data):
    author = data["author"]
    title = data["title"]
    body = data["text"]
    publish_date = data["published"]
    image_url = data["thread"]["main_image"]
    url = data["url"]
    return Article(author=author, title=title, body=body, publish_date=publish_date, image_url=image_url, url=url)

def get_all_news() -> list[Article]:
    """Get all news articles from the datastore."""
    # 1. Use Redis client to fetch all articles
    redis = REDIS_CLIENT.get_entry("all_articles")
    # 2. Format the data into articles
    articles = []
    if not redis:
        return articles
    articles = [_format(data) for data in redis]
    # 3. Return a list of the articles formatted 
    return articles


def get_featured_news() -> Article | None:
    """Get the featured news article from the datastore."""
    # 1. Get all the articles
    articles = get_all_news()
    # 2. Return as a list of articles sorted by most recent date
    list.sort(articles, key=lambda obj: obj.publish_date, reverse=True)
    return articles
