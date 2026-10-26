# SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Test CI URL preparation using only the Python standard library."""

import ast
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


_ROOT = Path(__file__).resolve().parents[1]
_SCRIPT = _ROOT / ".github" / "scripts" / "prepare_pages_config.py"
_SPEC = importlib.util.spec_from_file_location("prepare_pages_config", _SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
prepare_config = _MODULE.prepare_config

_SOURCE = '''\
repository_owner = "FIXME"
repository_name = "FIXME"
page_url = f"https://{repository_owner}.github.io/{repository_name}"
project = "FIXME"
course_logo = {"image_light": "_static/FIXME"}
repository_url = f"https://github.com/{repository_owner}/{repository_name}"
pages_url = f"{page_url}/index.html"
slides_url = f"{page_url}/slides/index.html"
'''


class TestPagesConfig(unittest.TestCase):
    """Cover automatic metadata, custom settings, and safe runner-only writes."""

    def test_real_configuration_generates_both_navigation_links(self) -> None:
        """Resolve the actual template's icon links without executing imports."""
        source = (_ROOT / "source" / "conf.py").read_text(encoding="utf-8")
        prepared = prepare_config(
            source, "CourseTeam/WorkshopTemplate", "https://courses.example.org/demo/"
        )
        names = {
            "repository_owner", "repository_name", "repository_url", "page_url",
            "pages_icon", "slides_icon", "discuss_icon", "course_logo",
        }
        assignments = [
            statement
            for statement in ast.parse(prepared).body
            if isinstance(statement, ast.Assign)
            and all(
                isinstance(target, ast.Name) and target.id in names
                for target in statement.targets
            )
        ]
        namespace: dict[str, object] = {}
        module = ast.Module(body=assignments, type_ignores=[])
        exec(compile(module, "conf.py", "exec"), namespace)
        self.assertEqual(
            namespace["pages_icon"]["url"],
            "https://courses.example.org/demo/index.html",
        )
        self.assertEqual(
            namespace["slides_icon"]["url"],
            "https://courses.example.org/demo/slides/index.html",
        )
        self.assertEqual(
            namespace["repository_url"],
            "https://github.com/CourseTeam/WorkshopTemplate",
        )

    def test_repository_casing_and_unrelated_placeholders(self) -> None:
        """Use GitHub metadata without replacing other template FIXME values."""
        prepared = prepare_config(
            _SOURCE, "CourseTeam/MixedCase", "https://example.org/site/"
        )
        self.assertIn("repository_owner = 'CourseTeam'", prepared)
        self.assertIn("repository_name = 'MixedCase'", prepared)
        self.assertIn("page_url = 'https://example.org/site'", prepared)
        self.assertIn('project = "FIXME"', prepared)
        self.assertIn('"image_light": "_static/FIXME"', prepared)

    def test_custom_values_remain_byte_for_byte_unchanged(self) -> None:
        """Do not override a configured repository or custom site URL."""
        custom = _SOURCE.replace('"FIXME"', '"custom"').replace(
            'f"https://{repository_owner}.github.io/{repository_name}"',
            '"https://custom.example.org/course/"',
        )
        self.assertEqual(
            prepare_config(custom, "Other/Repo", "https://example.org"), custom
        )

    def test_quotes_comments_annotations_and_unicode_are_preserved(self) -> None:
        """Rewrite AST value spans, not whole lines or matching strings elsewhere."""
        source = _SOURCE.replace(
            'repository_owner = "FIXME"',
            'label = "🌐"; repository_owner: str = \'FIXME\'  # keep this comment',
        ).replace("\n", "\r\n")
        prepared = prepare_config(source, "CourseTeam/Docs", "https://example.org")
        self.assertIn(
            'label = "🌐"; repository_owner: str = \'CourseTeam\'  '
            '# keep this comment\r\n',
            prepared,
        )
        self.assertEqual(prepared.count("\r\n"), source.count("\r\n"))

    def test_root_site_and_repeated_preparation(self) -> None:
        """Handle an organisation site and make a repeated run a no-op."""
        prepared = prepare_config(
            _SOURCE, "CourseTeam/Docs", "https://courseteam.github.io/"
        )
        self.assertIn("page_url = 'https://courseteam.github.io'", prepared)
        self.assertEqual(
            prepare_config(prepared, "CourseTeam/Docs", "https://example.org"),
            prepared,
        )

    def test_missing_or_malformed_metadata_is_rejected(self) -> None:
        """Fail rather than silently produce invalid deployment URLs."""
        for repository in ("", "owner", "/repo", "owner/", "a/b/c", "owner/a b"):
            with self.subTest(repository=repository), self.assertRaises(ValueError):
                prepare_config(_SOURCE, repository, "https://example.org")
        for url in (
            "", "example.org", "file:///tmp/site", "https://example.org?q=x",
            "https://example.org/#x", "https://user:pass@example.org",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                prepare_config(_SOURCE, "CourseTeam/Docs", url)

    def test_missing_duplicate_and_chained_settings_are_rejected(self) -> None:
        """Avoid ambiguous edits or unintended changes to another variable."""
        cases = (
            _SOURCE.replace('repository_name = "FIXME"\n', ""),
            _SOURCE + 'repository_name = "second"\n',
            _SOURCE.replace(
                'repository_name = "FIXME"',
                'repository_name = other = "FIXME"',
            ),
        )
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                prepare_config(source, "CourseTeam/Docs", "https://example.org")

    def test_cli_uses_environment_and_does_not_write_on_failure(self) -> None:
        """Exercise the CI entry point against a disposable configuration."""
        with TemporaryDirectory() as directory:
            config = Path(directory) / "conf.py"
            config.write_text(_SOURCE, encoding="utf-8")
            environment = dict(os.environ, GITHUB_REPOSITORY="", PAGES_BASE_URL="")
            result = subprocess.run(
                [sys.executable, str(_SCRIPT), str(config)],
                env=environment, capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("GITHUB_REPOSITORY", result.stderr)
            self.assertEqual(config.read_text(encoding="utf-8"), _SOURCE)
            environment.update(
                GITHUB_REPOSITORY="CourseTeam/Docs",
                PAGES_BASE_URL="https://example.org/site",
            )
            subprocess.run(
                [sys.executable, str(_SCRIPT), str(config)],
                env=environment, check=True,
            )
            self.assertIn(
                "page_url = 'https://example.org/site'",
                config.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
