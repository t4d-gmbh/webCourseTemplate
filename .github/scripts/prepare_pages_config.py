# SPDX-FileCopyrightText: 2023-2026 Jonas I. Liechti <j-i-l@t4d.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Resolve template URL placeholders in the CI checkout before Sphinx builds."""

import argparse
import ast
import os
from pathlib import Path
from urllib.parse import urlsplit


_DEFAULT_PAGE_URL = ast.parse(
    'f"https://{repository_owner}.github.io/{repository_name}"', mode="eval"
).body


def prepare_config(source: str, repository: str, base_url: str) -> str:
    """Resolve default deployment settings without changing custom settings.

    Parameters
    ----------
    source : str
        Contents of the template's Sphinx configuration file.
    repository : str
        GitHub's ``GITHUB_REPOSITORY`` value, in ``owner/name`` form.
    base_url : str
        Full site URL returned by ``actions/configure-pages``. A trailing
        slash is removed before constructing links.

    Returns
    -------
    str
        Configuration with placeholder owner/name values and the default
        Pages URL expression replaced. All other source text is preserved.

    Raises
    ------
    ValueError
        If metadata is missing or malformed, or a required setting does not
        have exactly one top-level assignment.
    SyntaxError
        If the configuration is not valid Python.
    """
    parts = repository.split("/")
    if len(parts) != 2 or not all(parts) or any(c.isspace() for c in repository):
        raise ValueError("GITHUB_REPOSITORY must contain owner/repository")
    url = urlsplit(base_url)
    if (
        url.scheme not in {"http", "https"}
        or not url.netloc
        or url.username is not None
        or url.password is not None
        or url.query
        or url.fragment
        or any(c.isspace() for c in base_url)
    ):
        raise ValueError("PAGES_BASE_URL must be an absolute HTTP(S) site URL")

    replacements = {
        "repository_owner": parts[0],
        "repository_name": parts[1],
        "page_url": base_url.rstrip("/"),
    }
    assignments: dict[str, list[ast.expr]] = {name: [] for name in replacements}
    for statement in ast.parse(source).body:
        if isinstance(statement, ast.Assign):
            targets, value = statement.targets, statement.value
        elif isinstance(statement, ast.AnnAssign) and statement.value is not None:
            targets, value = [statement.target], statement.value
        else:
            continue
        for target in targets:
            if isinstance(target, ast.Name) and target.id in assignments:
                # Rewriting a chained assignment would change another setting.
                if len(targets) != 1:
                    raise ValueError(f"{target.id} must have its own assignment")
                assignments[target.id].append(value)

    # AST column offsets count UTF-8 bytes, not Unicode characters.
    encoded = source.encode("utf-8")
    lines = encoded.splitlines(keepends=True)
    edits: list[tuple[int, int, bytes]] = []
    for name, values in assignments.items():
        if len(values) != 1:
            raise ValueError(f"Expected exactly one top-level assignment for {name}")
        value = values[0]
        if name == "page_url":
            is_default = ast.dump(value) == ast.dump(_DEFAULT_PAGE_URL)
        else:
            is_default = isinstance(value, ast.Constant) and value.value == "FIXME"
        if not is_default:
            continue
        assert value.end_lineno is not None and value.end_col_offset is not None
        start = sum(map(len, lines[: value.lineno - 1])) + value.col_offset
        end = sum(map(len, lines[: value.end_lineno - 1])) + value.end_col_offset
        edits.append((start, end, repr(replacements[name]).encode("utf-8")))
    for start, end, replacement in sorted(edits, reverse=True):
        encoded = encoded[:start] + replacement + encoded[end:]
    prepared = encoded.decode("utf-8")
    ast.parse(prepared)
    return prepared


def _main() -> None:
    """Prepare the runner's configuration, failing before writes on bad input."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", nargs="?", type=Path, default=Path("source/conf.py"))
    arguments = parser.parse_args()
    with arguments.config.open(encoding="utf-8", newline="") as handle:
        source = handle.read()
    try:
        prepared = prepare_config(
            source,
            os.environ.get("GITHUB_REPOSITORY", ""),
            os.environ.get("PAGES_BASE_URL", ""),
        )
    except (ValueError, SyntaxError) as error:
        parser.error(str(error))
    with arguments.config.open("w", encoding="utf-8", newline="") as handle:
        handle.write(prepared)


if __name__ == "__main__":
    _main()
