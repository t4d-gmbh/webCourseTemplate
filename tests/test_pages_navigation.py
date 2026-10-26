# SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Check actual navigation links after both Sphinx HTML builds have completed."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest


_ROOT = Path(__file__).resolve().parents[1]


class _NavigationLinks(HTMLParser):
    """Collect only the theme's page/slide navigation icons, not code examples."""

    def __init__(self) -> None:
        super().__init__()
        self.links: dict[str, list[str]] = {"Pages": [], "Slides": []}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Collect navigation anchor attributes supplied by the HTML parser."""
        attributes = dict(attrs)
        title = attributes.get("title")
        classes = (attributes.get("class") or "").split()
        if tag == "a" and title in self.links and "pst-navbar-icon" in classes:
            self.links[title].append(attributes.get("href") or "")


class TestPagesNavigation(unittest.TestCase):
    """Reject missing, placeholder, or inconsistent deployed navigation URLs."""

    def test_built_pages_and_slides_link_to_each_other(self) -> None:
        """Validate the two built entry points without modifying source files."""
        bases = []
        for path, title, suffix in (
            ("docs/html/index.html", "Slides", "/slides/index.html"),
            ("docs/html/slides/index.html", "Pages", "/index.html"),
        ):
            with self.subTest(path=path):
                parser = _NavigationLinks()
                parser.feed((_ROOT / path).read_text(encoding="utf-8"))
                self.assertEqual(len(parser.links[title]), 1)
                link = parser.links[title][0]
                url = urlsplit(link)
                self.assertIn(url.scheme, {"http", "https"})
                self.assertTrue(url.hostname)
                self.assertNotEqual(url.hostname.split(".")[0].lower(), "fixme")
                self.assertNotIn("fixme", url.path.lower().split("/"))
                self.assertFalse(url.query or url.fragment)
                self.assertTrue(link.endswith(suffix), link)
                bases.append(link.removesuffix(suffix))
        self.assertEqual(len(bases), 2)
        self.assertEqual(bases[0], bases[1])


if __name__ == "__main__":
    unittest.main()
