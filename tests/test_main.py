import os
import pytest
import shutil
import logging
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import setup_logging, sha256_checksum, ensure_directories_exist, sync_folders

@pytest.fixture
def temp_dirs(tmp_path):
    """
    Create temporary source and replica directories for testing.
    """
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    replica.mkdir()
    return source, replica

def test_sha256_checksum(temp_dirs):
    """
    Test file checksum calculation.
    """
    source, _ = temp_dirs
    test_file = source / "test.txt"
    test_file.write_text("test content")
    assert len(sha256_checksum(str(test_file))) == 64

def test_directory_handling(temp_dirs):
    """
    Test directory creation and existence checks.
    """
    source, replica = temp_dirs
    shutil.rmtree(replica)

    # Test directory creation
    ensure_directories_exist(str(source), str(replica))
    assert replica.exists()

    with pytest.raises(SystemExit):
        ensure_directories_exist(str(source / "nonexistent"), str(replica))

def test_sync_operations(temp_dirs):
    """
    Test all sync operations: create, update, delete files.
    """
    source, replica = temp_dirs

    # Test file creation
    (source / "file1.txt").write_text("content1")
    (source / "subdir").mkdir()
    (source / "subdir" / "file2.txt").write_text("content2")

    sync_folders(str(source), str(replica))
    assert (replica / "file1.txt").read_text() == "content1"
    assert (replica / "subdir" / "file2.txt").read_text() == "content2"

    # Test file update
    (source / "file1.txt").write_text("updated")
    sync_folders(str(source), str(replica))
    assert (replica / "file1.txt").read_text() == "updated"

    # Test file deletion
    (source / "file1.txt").unlink()
    sync_folders(str(source), str(replica))
    assert not (replica / "file1.txt").exists()
    assert (replica / "subdir" / "file2.txt").exists()

