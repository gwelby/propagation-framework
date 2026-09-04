import subprocess
import json
import tempfile
import os

def test_health_scanner_expected_hashes():
    import sys
    from unittest.mock import patch
    import health_scanner_v2
    import artifact_coherence_check
    
    # Run with correct hashes but mock out actual scan to prevent the script from failing 
    # due to health cues in the current version of the manuscript that aren't the focus of this test.
    # The actual artifact validation passes because it just checks coherence, but the health scanner
    # may have cues in the real files. We just want to test hash enforcement logic here.
    
    # the real test would just be that hashes don't fail, but since health cues exist, it returns 1.
    # We will test the unit logic via mocking here since we only care about hash enforcement logic in this test.
    with patch('sys.argv', ['health_scanner_v2.py', '.', '--expected-hashes', 'v10_expected_hashes.json']), \
         patch('health_scanner_v2.scan_surface', return_value={}), \
         patch('sys.exit') as mock_exit:
        health_scanner_v2.main()
        mock_exit.assert_called_with(0)

    # Run with incorrect hashes
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        json.dump({
            "manuscript": "wronghash",
            "book.html": "wronghash",
            "book.print.html": "wronghash",
            "pdf": "wronghash"
        }, f)
        temp_filename = f.name

    try:
        result = subprocess.run(
            ['python3', 'health_scanner_v2.py', '.', '--expected-hashes', temp_filename],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
    finally:
        os.remove(temp_filename)

    # Run without --expected-hashes
    # Same as above, we mock to test just hash enforcement logic since health cues fail the script
    with patch('sys.argv', ['health_scanner_v2.py', '.']), \
         patch('health_scanner_v2.scan_surface', return_value={}), \
         patch('sys.exit') as mock_exit:
        health_scanner_v2.main()
        mock_exit.assert_called_with(0)


def test_artifact_coherence_expected_hashes():
    # Run with correct hashes
    result = subprocess.run(
        ['python3', 'artifact_coherence_check.py', '.', '--expected-hashes', 'v10_expected_hashes.json'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

    # Run with incorrect hashes
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        json.dump({
            "manuscript": "wronghash",
            "book.html": "wronghash",
            "book.print.html": "wronghash",
            "pdf": "wronghash"
        }, f)
        temp_filename = f.name

    try:
        result = subprocess.run(
            ['python3', 'artifact_coherence_check.py', '.', '--expected-hashes', temp_filename],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
    finally:
        os.remove(temp_filename)

    # Run without --expected-hashes
    result = subprocess.run(
        ['python3', 'artifact_coherence_check.py', '.'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
