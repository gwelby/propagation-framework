import subprocess

def test_git_archive_contains_agents_full():
    result = subprocess.run(
        "git archive HEAD | tar -t",
        shell=True,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "AGENTS_FULL.md" in result.stdout.splitlines()
