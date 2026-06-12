"""Tests for the Markdown parser."""

import pytest

from docs_linter.parsers.markdown import MarkdownParser


@pytest.fixture
def parser():
    return MarkdownParser()


def test_skips_fenced_code_blocks(parser):
    content = """Some prose here.

```python
This is code and should not be linted.
The the doubled word is fine in code.
```

More prose after code.
"""
    lines = parser.parse(content)
    texts = [line.text for line in lines]
    assert any("prose here" in t for t in texts)
    assert any("prose after" in t for t in texts)
    assert not any("code and should" in t for t in texts)


def test_skips_frontmatter(parser):
    content = """---
title: My Document
author: Test
---

This is the actual content.
"""
    lines = parser.parse(content)
    texts = [line.text for line in lines]
    assert not any("title:" in t for t in texts)
    assert any("actual content" in t for t in texts)


def test_strips_inline_code(parser):
    content = "Use the `will_not_flag` function to start.\n"
    lines = parser.parse(content)
    assert len(lines) == 1
    assert "`will_not_flag`" not in lines[0].text


def test_preserves_line_numbers(parser):
    content = """Line one.

Line three.


Line six.
"""
    lines = parser.parse(content)
    line_nums = [line.line_num for line in lines]
    assert 1 in line_nums
    assert 3 in line_nums
    assert 6 in line_nums


def test_identifies_headings(parser):
    content = """# Main heading

Some paragraph text.

## Subheading
"""
    lines = parser.parse(content)
    headings = [line for line in lines if line.is_heading]
    non_headings = [line for line in lines if not line.is_heading]
    assert len(headings) == 2
    assert len(non_headings) == 1


def test_skips_indented_code(parser):
    content = """Normal text.

    indented_code_block = True
    should_be_skipped = True

Back to prose.
"""
    lines = parser.parse(content)
    texts = [line.text for line in lines]
    assert not any("indented_code" in t for t in texts)
    assert any("Normal text" in t for t in texts)
    assert any("Back to prose" in t for t in texts)


def test_removes_urls(parser):
    content = "Visit https://example.com/docs/guide for more info.\n"
    lines = parser.parse(content)
    assert "https://example.com" not in lines[0].text
