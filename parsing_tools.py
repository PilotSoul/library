import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
import urllib.request
import re
from datetime import datetime

# urls = [f'https://ilibrary.ru/text/{i}/index.html' for i in range(1, 500)] #4540
author_url = "https://ilibrary.ru/author.html"
books = {}


async def get_author_info(author):
    url = author.get("href")
    name = author.get_text().replace("\xa0", " ")
    id = re.fullmatch(r"/author/([^/]+)/index.html", url).group(1)
    urls = f"/author/{id}/l.all/index.html"
    return name, urls


async def make_json(unique_num: int, name, url, b_date, title):
    """
    :param unique_num: id книги
    :param name: имя автора
    :param url: url на книгу
    :param b_date: дата выпуска
    :param title: название книги
    """
    with open(f"books/{unique_num}.json", "w") as file:
        json.dump({
            "author_name": name,
            "book_url": url,
            "issue_date": b_date,
            "book_title": title
        }, file)


async def get_date_of_issue(url: str):
    with urllib.request.urlopen(url) as response:
        about_soup = BeautifulSoup(response.read(), "html.parser")
    caption = about_soup.select(".tabout > i:first-child")[0]
    if caption.get_text() == "Даты написания:":
        book_date = caption.next_sibling.removesuffix(".")
    else:
        book_date = 'Без Даты'
    return book_date


async def get_writer_info(writer):
    url = writer.get("href")
    title = writer.get_text()
    id = int(re.match(r"/text/([1-9]\d*)/p.1/index.html", url).group(1))
    return title, id


async def main(author_url):
    with urllib.request.urlopen(author_url) as response:
        soup = BeautifulSoup(response.read(), "html.parser")
    for author in soup.select(".alst a"):
        author_name, book_urls = await get_author_info(author)
        # книги по каждому автору
        full_book_urls = "https://ilibrary.ru" + book_urls
        with urllib.request.urlopen(full_book_urls) as response:
            all_soup = BeautifulSoup(response.read(), "html.parser")
        for book in all_soup.select("#text a"):
            book_title = book.get_text()
            book_url = book.get("href")
            try:
                # через соответствие шаблону
                book_id = int(re.match(r"/text/([1-9]\d*)/p.1/index.html", book_url).group(1))
            except:
                continue
            about_url = f"https://ilibrary.ru/text/{book_id}/index.html"
            date_of_issue = await get_date_of_issue(about_url)
            await make_json(book_id, author_name, book_url, date_of_issue, book_title)
    return "Successful"


if __name__ == '__main__':
    print(asyncio.run(main(author_url)))