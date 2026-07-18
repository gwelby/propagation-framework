"""Unit tests for assemble_manuscript.py source map parsing and bounding.

Proves:
1. Bounding of parse_source_map() between ## FRONT MATTER and # PART IV — AGENT PROTOCOLS.
2. Excludes Part IV tables and entries.
3. Fails closed (raises ValueError) if either ## FRONT MATTER or # PART IV — AGENT PROTOCOLS is absent.
4. Excludes derivations/*.md from the parsed entries.
"""

import sys
from pathlib import Path
import pytest

# Ensure fundamentals root is in path to import assemble_manuscript
BASE_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from assemble_manuscript import parse_source_map


def test_parse_source_map_success(tmp_path):
    """Test successful parsing of a bounded source map."""
    agents_content = """# Title
Some intro text.

## FRONT MATTER

| Section | Source |
|---------|--------|
| Title Page | Generate from this AGENTS.md metadata |
| Epigraph | `the_propagation_framework.md` |

## PART ONE — THE QUESTION

| Chapter | Content | Source |
|---------|---------|--------|
| 1. Intro | Plain language | `the_propagation_framework.md` |

# PART IV — AGENT PROTOCOLS

## THE ONE RULE
INGEST before WRITE.

| Agent | Role | Output Format |
|-------|------|--------------|
| Claude | Synthesis | derivations/*.md |
"""
    agents_file = tmp_path / "AGENTS_FULL_TEST.md"
    agents_file.write_text(agents_content, encoding="utf-8")

    entries = parse_source_map(path=agents_file)
    
    # Check that we parsed the correct entries from the source map
    assert len(entries) == 3
    assert entries[0]["title"] == "Title Page"
    assert entries[0]["source"] == "Generate from this AGENTS.md metadata"
    assert entries[1]["title"] == "Epigraph"
    assert entries[1]["source"] == "`the_propagation_framework.md`"
    assert entries[2]["title"] == "1. Intro"
    assert entries[2]["source"] == "`the_propagation_framework.md`"

    # Check that we did NOT parse the derivations/*.md from PART IV
    for entry in entries:
        assert "derivations/*.md" not in entry["source"]
        assert "Claude" not in entry["title"]


def test_parse_source_map_hyphen_marker(tmp_path):
    """Test successful parsing when using the hyphen variation of PART IV."""
    agents_content = """## FRONT MATTER
| Section | Source |
| Title Page | metadata |

# PART IV - AGENT PROTOCOLS
| Claude | Synthesis | derivations/*.md |
"""
    agents_file = tmp_path / "AGENTS_FULL_TEST_HYPHEN.md"
    agents_file.write_text(agents_content, encoding="utf-8")

    entries = parse_source_map(path=agents_file)
    assert len(entries) == 1
    assert entries[0]["title"] == "Title Page"


def test_parse_source_map_missing_front_matter(tmp_path):
    """Test that parse_source_map raises ValueError if FRONT MATTER is missing."""
    agents_content = """# PART IV — AGENT PROTOCOLS
| Section | Source |
"""
    agents_file = tmp_path / "AGENTS_FULL_MISSING_FM.md"
    agents_file.write_text(agents_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Could not find ## FRONT MATTER"):
        parse_source_map(path=agents_file)


def test_parse_source_map_missing_end_marker(tmp_path):
    """Test that parse_source_map raises ValueError if PART IV end marker is missing."""
    agents_content = """## FRONT MATTER
| Section | Source |
"""
    agents_file = tmp_path / "AGENTS_FULL_MISSING_END.md"
    agents_file.write_text(agents_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Could not find # PART IV — AGENT PROTOCOLS"):
        parse_source_map(path=agents_file)


def test_parser_excludes_part_iv_and_derivations_glob(tmp_path):
    """NEGATIVE FIXTURE: Explicitly proves that Part IV and any derivations/*.md within it cannot enter the parsed map."""
    agents_content = """## FRONT MATTER
| Section | Source |
| Front Section | `some_file.md` |

# PART IV — AGENT PROTOCOLS
## CLAIM STATUS PROTOCOL
| Status | Meaning |
| **DERIVED** | derivations/*.md |
"""
    agents_file = tmp_path / "AGENTS_FULL_ISOLATED_FIXTURE.md"
    agents_file.write_text(agents_content, encoding="utf-8")

    entries = parse_source_map(path=agents_file)
    assert len(entries) == 1
    assert entries[0]["title"] == "Front Section"
    assert entries[0]["source"] == "`some_file.md`"
    
    # Assert absolutely no presence of Part IV data in the parsed entries
    for entry in entries:
        assert "derivations/*.md" not in entry["source"]
        assert "derivations/*.md" not in entry["title"]
        assert "DERIVED" not in entry["title"]
        assert "DERIVED" not in entry["source"]
