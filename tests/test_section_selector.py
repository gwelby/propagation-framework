import pytest
from assemble_manuscript import extract_section

TEST_CONTENT = """# Main Document

## 6

This is the content for section 6.

### 6.1

This is the content for section 6.1.

### 6.2

This is the content for section 6.2.

### 6.3

This is the content for section 6.3.

## 7

This is section 7.
"""

def test_extract_section_6_1():
    result = extract_section(TEST_CONTENT, '§6.1')
    assert "This is the content for section 6.1." in result
    assert "This is the content for section 6.2." not in result
    assert "This is the content for section 6.3." not in result
    assert "## 6\n" not in result
    assert "### 6.1" in result

def test_extract_section_6():
    result = extract_section(TEST_CONTENT, '§6')
    assert "This is the content for section 6." in result
    assert "### 6.1" in result
    assert "This is the content for section 6.1." in result
    assert "### 6.2" in result
    assert "This is the content for section 6.2." in result
    assert "### 6.3" in result
    assert "This is the content for section 6.3." in result
    assert "## 7" not in result
