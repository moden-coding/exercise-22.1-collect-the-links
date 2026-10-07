#!/usr/bin/env python3
"""Tests for Exercise 23: Collect the Links. These never touch the network."""

import os
import unittest

from src.collect_links import BASE, game_urls, load_soup, page_urls

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")

ALL_PAGES = {BASE + f"page-{n}.html" for n in range(1, 13)}

PAGE_1_GAMES = {
    BASE + "game-lantern-harbor.html",
    BASE + "game-cobblestone-kings.html",
    BASE + "game-moss-and-mortar.html",
    BASE + "game-starlit-orchard.html",
    BASE + "game-7-lanterns.html",
    BASE + "game-thimble-thieves.html",
    BASE + "game-copper-canyon-express.html",
    BASE + "game-quill-and-ink.html",
    BASE + "game-penguin-parade.html",
    BASE + "game-volcano-bakers.html",
}

DECOYS = {
    BASE + "about.html",
    BASE + "events.html",
    BASE + "page-turners-book-club.html",
    BASE + "menu.html",
}


def fixture(name):
    return load_soup(os.path.join(FIXTURES, name))


class UrlChecks(unittest.TestCase):
    """Shared checks that turn common mistakes into plain-English failures."""

    def check_list(self, result, name):
        self.assertIsNotNone(
            result,
            msg=f"{name} returned None. Did you forget the return statement?",
        )
        self.assertIsInstance(
            result,
            list,
            msg=f"{name} should return a list, but it returned a "
            f"{type(result).__name__}. If you built a set, turn it into a list "
            "before returning it.",
        )

    def check_full_urls(self, result, name):
        short = [u for u in result if not str(u).startswith("https://")]
        self.assertEqual(
            short,
            [],
            msg=f"{name}: these should be full URLs starting with https://, but "
            f"some are just the end of the link: {short[:3]}. Put BASE in front "
            "of each href.",
        )

    def check_no_duplicates(self, result, name):
        repeats = sorted({u for u in result if result.count(u) > 1})
        self.assertEqual(
            repeats,
            [],
            msg=f"{name}: a URL appears twice in your list: {repeats[:3]}. Some "
            "links show up more than once on the page; keep each URL only once.",
        )

    def check_no_decoys(self, result, name):
        decoys = sorted(set(result) & DECOYS)
        self.assertEqual(
            decoys,
            [],
            msg=f"{name}: a decoy link got in: {decoys}. Not every link with "
            "'page' in it is a catalog page.",
        )


class TestPageUrlsOnPage1(UrlChecks):
    """page_urls(soup) on catalog page 1."""

    def setUp(self):
        self.result = page_urls(fixture("page-1.html"))

    def test_returns_a_list(self):
        self.check_list(self.result, "page_urls")

    def test_full_urls(self):
        self.check_list(self.result, "page_urls")
        self.check_full_urls(self.result, "page_urls")

    def test_no_duplicates(self):
        self.check_list(self.result, "page_urls")
        self.check_no_duplicates(self.result, "page_urls")

    def test_no_decoys(self):
        self.check_list(self.result, "page_urls")
        self.check_no_decoys(self.result, "page_urls")

    def test_no_game_pages(self):
        self.check_list(self.result, "page_urls")
        games = sorted(u for u in self.result if "game-" in str(u))
        self.assertEqual(
            games,
            [],
            msg=f"page_urls: a game detail page got in: {games[:3]}. page_urls "
            "should only collect the catalog pages.",
        )

    def test_finds_12_pages(self):
        self.check_list(self.result, "page_urls")
        self.assertEqual(
            len(self.result),
            12,
            msg=f"page_urls found {len(self.result)} URLs on page 1, but the "
            "catalog has 12 pages.",
        )

    def test_exact_pages(self):
        self.check_list(self.result, "page_urls")
        missing = sorted(ALL_PAGES - set(self.result))
        extra = sorted(set(self.result) - ALL_PAGES)
        self.assertEqual(
            set(self.result),
            ALL_PAGES,
            msg=f"page_urls on page 1 should be exactly the 12 catalog pages. "
            f"Missing: {missing[:3]}  Should not be there: {extra[:3]}",
        )


class TestPageUrlsOnPage12(UrlChecks):
    """page_urls(soup) on catalog page 12, the last page, which has no Next link."""

    def setUp(self):
        self.result = page_urls(fixture("page-12.html"))

    def test_still_finds_all_12_pages(self):
        self.check_list(self.result, "page_urls")
        missing = sorted(ALL_PAGES - set(self.result))
        self.assertEqual(
            missing,
            [],
            msg=f"page_urls on page 12 is missing {missing[:3]}. Page 12 has no "
            "'Next' link, so don't rely on it: every page number is listed at "
            "the bottom of every page.",
        )
        self.check_full_urls(self.result, "page_urls")
        self.check_no_duplicates(self.result, "page_urls")
        self.check_no_decoys(self.result, "page_urls")
        self.assertEqual(
            len(self.result),
            12,
            msg=f"page_urls found {len(self.result)} URLs on page 12, but the "
            "catalog has 12 pages.",
        )


class TestGameUrlsOnPage1(UrlChecks):
    """game_urls(soup) on catalog page 1."""

    def setUp(self):
        self.result = game_urls(fixture("page-1.html"))

    def test_returns_a_list(self):
        self.check_list(self.result, "game_urls")

    def test_full_urls(self):
        self.check_list(self.result, "game_urls")
        self.check_full_urls(self.result, "game_urls")

    def test_no_duplicates(self):
        self.check_list(self.result, "game_urls")
        self.check_no_duplicates(self.result, "game_urls")

    def test_no_decoys(self):
        self.check_list(self.result, "game_urls")
        self.check_no_decoys(self.result, "game_urls")

    def test_no_catalog_pages(self):
        self.check_list(self.result, "game_urls")
        pages = sorted(set(self.result) & ALL_PAGES)
        self.assertEqual(
            pages,
            [],
            msg=f"game_urls: a catalog page got in: {pages[:3]}. game_urls "
            "should only collect game detail pages.",
        )

    def test_includes_game_with_a_number(self):
        self.check_list(self.result, "game_urls")
        self.assertIn(
            BASE + "game-7-lanterns.html",
            self.result,
            msg="game_urls is missing the '7 Lanterns' game. A game's name can "
            "have a number in it, so make sure your pattern doesn't skip it.",
        )

    def test_finds_10_games(self):
        self.check_list(self.result, "game_urls")
        self.assertEqual(
            len(self.result),
            10,
            msg=f"game_urls found {len(self.result)} URLs on page 1, but each "
            "catalog page lists 10 games.",
        )

    def test_exact_games(self):
        self.check_list(self.result, "game_urls")
        missing = sorted(PAGE_1_GAMES - set(self.result))
        extra = sorted(set(self.result) - PAGE_1_GAMES)
        self.assertEqual(
            set(self.result),
            PAGE_1_GAMES,
            msg=f"game_urls on page 1 should be exactly its 10 games. "
            f"Missing: {missing[:3]}  Should not be there: {extra[:3]}",
        )


if __name__ == "__main__":
    unittest.main()
