"""The fallback crawler starts from the exact URL the user trains on."""

import pytest

from harvey.trainer import FallbackCrawler


@pytest.mark.asyncio
async def test_crawl_includes_unlinked_start_page(monkeypatch):
    fetched: list[str] = []

    async def fake_fetch(self, client, url):
        fetched.append(url)
        return "<html></html>", f"text of {url}"

    monkeypatch.setattr(FallbackCrawler, "_fetch_page", fake_fetch)

    start = "https://example.com/beta-22435/"
    pages = await FallbackCrawler().crawl(
        "https://example.com", max_pages=1, start_url=start
    )

    assert fetched[0] == start
    assert list(pages) == [start]
