# Exercise 23: Collect the Links

## The goal

Before you can scrape every page of a site, you need a list of every page.
Today you'll collect the full URL of every catalog page, and of every game on
page 1.

## The site

https://moden-coding.github.io/scrape-practice-site/catalog/page-1.html

Open it and Inspect the links at the bottom of the page.

## What to write

In `src/collect_links.py`:

- `page_urls(soup)`: the full URLs of all the catalog pages. Expect **12**.
- `game_urls(soup)`: the full URLs of the game detail pages on this page. Expect **10**.

Both return a list with no duplicates. Leave the toolkit at the top alone.

## Watch out for

- Some links appear twice.
- Not every link with "page" in it is a page.
- You need the full URL, not just the end of it.

## Run it

```
python src/collect_links.py
python -m unittest discover
```

## Done when

All tests pass and `main()` prints 12 pages and 10 games.
