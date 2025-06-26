"""
Tests for the utils module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from psuedo_lammps.utils import (
    validate_lammps_file,
    safe_get,
    ensure_directory,
    list_lammps_files,
    extract_box_bounds,
    calculate_center_of_mass,
)


def test_validate_lammps_file_with_valid_file(tmp_path):
    """Test validate_lammps_file with a valid LAMMPS dump file."""
    dump_file = tmp_path / "test.dump"
    with open(dump_file, 'w') as f:
        f.write("ITEM: TIMESTEP\n1000\n")
    
    assert validate_lammps_file(dump_file) is True


def test_validate_lammps_file_with_invalid_file(tmp_path):
    """Test validate_lammps_file with an invalid file."""
    invalid_file = tmp_path / "test.txt"
    with open(invalid_file, 'w') as f:
        f.write("This is not a LAMMPS dump file\n")
    
    assert validate_lammps_file(invalid_file) is False


def test_validate_lammps_file_nonexistent():
    """Test validate_lammps_file with nonexistent file."""
    assert validate_lammps_file("nonexistent.dump") is False


def test_safe_get_existing_key():
    """Test safe_get with existing key."""
    data = {"a": 1, "b": 2}
    assert safe_get(data, "a") == 1
    assert safe_get(data, "b") == 2


def test_safe_get_missing_key():
    """Test safe_get with missing key."""
    data = {"a": 1, "b": 2}
    assert safe_get(data, "c") is None
    assert safe_get(data, "c", "default") == "default"


def test_ensure_directory_creates_new_directory(tmp_path):
    """Test ensure_directory creates new directory."""
    new_dir = tmp_path / "new_directory"
    result = ensure_directory(new_dir)
    
    assert result.exists()
    assert result.is_dir()
    assert result == new_dir


def test_ensure_directory_existing_directory(tmp_path):
    """Test ensure_directory with existing directory."""
    existing_dir = tmp_path / "existing"
    existing_dir.mkdir()
    
    result = ensure_directory(existing_dir)
    assert result == existing_dir


def test_list_lammps_files_empty_directory(tmp_path):
    """Test list_lammps_files with empty directory."""
    files = list_lammps_files(tmp_path)
    assert files == []


def test_list_lammps_files_with_valid_files(tmp_path):
    """Test list_lammps_files with valid LAMMPS dump files."""
    # Create valid LAMMPS dump files
    dump_file1 = tmp_path / "file1.dump"
    with open(dump_file1, 'w') as f:
        f.write("ITEM: TIMESTEP\n1000\n")
    
    dump_file2 = tmp_path / "file2.dump"
    with open(dump_file2, 'w') as f:
        f.write("ITEM: TIMESTEP\n2000\n")
    
    # Create an invalid file
    invalid_file = tmp_path / "file3.txt"
    with open(invalid_file, 'w') as f:
        f.write("Not a LAMMPS file\n")
    
    files = list_lammps_files(tmp_path, "*.dump")
    assert len(files) == 2
    assert all(f.name.endswith(".dump") for f in files)


def test_extract_box_bounds():
    """Test extract_box_bounds returns correct structure."""
    data = pd.DataFrame()  # Empty DataFrame for now
    bounds = extract_box_bounds(data)
    
    expected_keys = ['xlo', 'xhi', 'ylo', 'yhi', 'zlo', 'zhi']
    assert all(key in bounds for key in expected_keys)
    assert all(isinstance(bounds[key], list) for key in expected_keys)


def test_calculate_center_of_mass_missing_mass_column():
    """Test calculate_center_of_mass raises error for missing mass column."""
    data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 2, 3], 'z': [1, 2, 3]})
    
    with pytest.raises(ValueError, match="Mass column 'mass' not found in data"):
        calculate_center_of_mass(data)


def test_calculate_center_of_mass_returns_array():
    """Test calculate_center_of_mass returns numpy array."""
    data = pd.DataFrame({
        'x': [1, 2, 3], 
        'y': [1, 2, 3], 
        'z': [1, 2, 3],
        'mass': [1, 1, 1]
    })
    
    com = calculate_center_of_mass(data)
    assert isinstance(com, np.ndarray)
    assert com.shape == (3,) 