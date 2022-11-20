import os
import json
import re
import asyncio


def parse_date(book_date):
    parsed_date = book_date.strip().rstrip(".").replace("\xa0", " ")
    match_year = re.fullmatch(r"(\d{4})(?: г)?", parsed_date)
    if match_year is not None:
        return [int(match_year.group(1))]

    match_month = re.fullmatch(r"\d{1,2} ?[а-яёА-ЯЁ]*,? (\d{4})(?: г)?", parsed_date)
    if match_month is not None:
        return [int(match_month.group(1))]

    match_arabic = re.fullmatch(r"(?:\d{1,2}[\. ])?(?:[IVX]+|\d+)[\. ](\d{4})", parsed_date)
    if match_arabic is not None:
        return [int(match_arabic.group(1))]

    match_arabic = re.fullmatch(r"(?:\d{1,2}[\. ])?(?:[IVX]+|\d+)[\. ](\d{2})", parsed_date)
    if match_arabic is not None:
        return [1900 + int(match_arabic.group(1))]

    match_period = re.fullmatch(r"(\d{4})—(\d{4}) гг", parsed_date)
    if match_period is not None:
        return list(range(int(match_period.group(1)), int(match_period.group(2))))

    match_period = re.fullmatch(r"(\d{4}), *(\d{4})", parsed_date)
    if match_period is not None:
        return [int(match_period.group(1)), int(match_period.group(2))]

    return [None]


def prepare_dates():
    books_by_date = {}
    books_titles = {}
    index = 0
    for file_name in os.listdir("books"):
        with open(f"books/{file_name}") as file:
            description = json.load(file)
            book_url = "https://ilibrary.ru" + description["book_url"]
            books_titles[book_url] = description["author_name"] + " - " + description["book_title"]
            if description["issue_date"] is None:
                b_dates = [f"WO_{index}"]
                index += 1
            else:
                b_dates = parse_date(description["issue_date"])
            for b_date in b_dates:
                books_by_date.setdefault(b_date, [])
                books_by_date[b_date].append(book_url)
    return books_by_date, books_titles


def set_decades(books_by_date, books_titles):
    centuries = [18, 19, 20, 0]
    decades = {}
    for books in books_by_date.values():
        books.sort(key=books_titles.get)
    books_dates = []
    if None in books_by_date:
        books_dates.append(None)
    books_dates += sorted(books_by_date.keys() - {None})

    for c in centuries:
        start_year = (c - 1) * 100
        index = 0
        for i in range(10):
            decades.setdefault(c, [])
            rn = list(range(start_year + i * 10, start_year + (i + 1) * 10 + 1))
            for bs_date in books_dates:
                if c == 0:
                    print(bs_date)
                    try:
                        if bs_date is None:
                            decades[c].append("-" + str(index))
                            index += 1
                    except:
                        continue
                elif bs_date in rn:
                    decades[c].append(str(start_year + i * 10) + " - " + str(start_year + (i + 1) * 10))
                    break
    return decades, books_dates


def get_decades():
    bks_by_date, bks_titles = prepare_dates()
    book_decades, books_dates = set_decades(bks_by_date, bks_titles)
    return book_decades, books_dates, bks_by_date, bks_titles
