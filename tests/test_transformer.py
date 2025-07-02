import pytest
from pathlib import Path
from cfm.engine.transformer import apply_rules, load_rules

FIXTURE_PATH = Path("src/")
FIXTURE_PATH = Path("tests/fixtures/")
SAMPLE_FILE = FIXTURE_PATH / "input_sample.cpp"
SAMPLE_FILE= FIXTURE_PATH /"example.cpp"
RULES_FILE = "rules/cpp/qt5to6/qt5to6.json"

def test_load_rules():
    """Ensure rule file loads as a list with 'match' entries"""
    rules = load_rules(RULES_FILE)
    assert isinstance(rules, list)
    assert any("match" in rule for rule in rules)
    assert len(rules) > 0

def test_apply_rules_dry_run(tmp_path):
    """Dry-run should simulate rule application but not alter file"""
    test_file = tmp_path / "sample.cpp"
    test_file.write_text(SAMPLE_FILE.read_text())

    report = apply_rules(
        file_paths=[str(test_file)],
        rule_path=RULES_FILE,
        dry_run=True,
        backup=False,
        show_diff=False
    )

    assert report["total_files_changed"] >= 1
    assert str(test_file) in report["per_file"]
    # Ensure original file content was not changed
    assert test_file.read_text() == SAMPLE_FILE.read_text()

def test_apply_rules_real_fix(tmp_path):
    """Actual fix mode should alter the file"""
    test_file = tmp_path / "sample.cpp"
    test_file.write_text(SAMPLE_FILE.read_text())

    report = apply_rules(
        file_paths=[str(test_file)],
        rule_path=RULES_FILE,
        dry_run=False,
        backup=False,
        show_diff=False
    )

    assert report["total_files_changed"] >= 1
    assert str(test_file) in report["per_file"]
    # Confirm file content has changed
    assert test_file.read_text() != SAMPLE_FILE.read_text()

def test_backup_file_created(tmp_path):
    """Ensure backup is created if backup=True"""
    test_file = tmp_path / "sample.cpp"
    test_file.write_text(SAMPLE_FILE.read_text())

    apply_rules(
        file_paths=[str(test_file)],
        rule_path=RULES_FILE,
        dry_run=False,
        backup=True,
        show_diff=False
    )

    backup_path = tmp_path / "sample.cpp.bak"
    assert backup_path.exists()
    assert backup_path.read_text() == SAMPLE_FILE.read_text()

def test_invalid_rule_path():
    """Should raise error or return empty if rule file is invalid"""
    with pytest.raises(FileNotFoundError):
        load_rules("rules/cpp/nonexistent.json")

def test_apply_rules_multiple_files(tmp_path):
    """Test rule application on multiple files"""
    test1 = tmp_path / "file1.cpp"
    test2 = tmp_path / "file2.cpp"
    content = SAMPLE_FILE.read_text()
    test1.write_text(content)
    test2.write_text(content)

    report = apply_rules(
        file_paths=[str(test1), str(test2)],
        rule_path=RULES_FILE,
        dry_run=True,
        backup=False,
        show_diff=False
    )

    assert report["total_files_changed"] == 2
    assert str(test1) in report["per_file"]
    assert str(test2) in report["per_file"]
