"""Markdown parser that extracts prose lines, skipping code blocks and frontmatter."""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class ProseLine:
    """A line of prose text with its original line number."""
    text: str
    line_num: int
    is_heading: bool = False


class MarkdownParser:
    """Extract prose from Markdown, skipping non-prose content.

    Skips:
        - YAML frontmatter (--- ... ---)
        - Fenced code blocks (``` or ~~~)
        - Indented code blocks (4+ spaces)
        - HTML comments (<!-- ... -->)
        - Inline code (backtick-wrapped text is stripped)
        - Raw URLs
        - Image alt text and link URLs
    """

    FENCED_CODE_START = re.compile(r"^\s*(`{3,}|~{3,})")
    FRONTMATTER_DELIM = re.compile(r"^---\s*$")
    INDENTED_CODE = re.compile(r"^(    |\t)\S")
    HTML_COMMENT_SINGLE = re.compile(r"<!--.*?-->")
    INLINE_CODE = re.compile(r"`[^`]+`")
    URL_PATTERN = re.compile(r"https?://\S+")
    LINK_URL = re.compile(r"\]\([^)]+\)")
    IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]+\)")

    def parse(self, content: str) -> List[ProseLine]:
        """Parse Markdown content and return prose lines.

        Args:
            content: Raw Markdown file content.

        Returns:
            List of ProseLine objects containing only lintable prose.
        """
        lines = content.split("\n")
        prose_lines = []

        in_frontmatter = False
        in_code_block = False
        code_fence_pattern = None
        frontmatter_started = False

        for i, line in enumerate(lines, start=1):
            # Handle YAML frontmatter (only at the very start of file)
            if i == 1 and self.FRONTMATTER_DELIM.match(line):
                in_frontmatter = True
                frontmatter_started = True
                continue

            if in_frontmatter:
                if self.FRONTMATTER_DELIM.match(line):
                    in_frontmatter = False
                continue

            # Handle fenced code blocks
            fence_match = self.FENCED_CODE_START.match(line)
            if fence_match:
                if not in_code_block:
                    in_code_block = True
                    code_fence_pattern = fence_match.group(1)[0]  # ` or ~
                elif line.strip().startswith(code_fence_pattern):
                    in_code_block = False
                continue

            if in_code_block:
                continue

            # Skip indented code blocks (4 spaces or tab)
            if self.INDENTED_CODE.match(line):
                continue

            # Skip empty lines
            if not line.strip():
                continue

            # Clean the line for linting
            clean_line = self._clean_line(line)

            if clean_line.strip():
                is_heading = line.strip().startswith("#")
                prose_lines.append(ProseLine(
                    text=clean_line,
                    line_num=i,
                    is_heading=is_heading,
                ))

        return prose_lines

    def _clean_line(self, line: str) -> str:
        """Remove non-prose elements from a line while preserving positions."""
        cleaned = line

        # Remove HTML comments
        cleaned = self.HTML_COMMENT_SINGLE.sub("", cleaned)

        # Remove images entirely
        cleaned = self.IMAGE_PATTERN.sub("", cleaned)

        # Remove link URLs but keep link text: [text](url) -> text
        cleaned = self.LINK_URL.sub("", cleaned)
        cleaned = cleaned.replace("[", "").replace("]", "")

        # Remove inline code
        cleaned = self.INLINE_CODE.sub("", cleaned)

        # Remove raw URLs
        cleaned = self.URL_PATTERN.sub("", cleaned)

        return cleaned
