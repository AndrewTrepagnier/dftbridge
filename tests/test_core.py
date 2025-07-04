"""
Tests for the core module.
"""

import pytest
import pandas as pd
from dftbridge.core import parse_lammps_dump, LAMMPSDumpParser


def test_parse_lammps_dump():
    """Test the parse_lammps_dump function returns a DataFrame."""
    result = parse_lammps_dump("nonexistent_file.dump")
    assert isinstance(result, pd.DataFrame)


def test_lammps_dump_parser_initialization():
    """Test LAMMPSDumpParser can be initialized with a file path."""
    file_path = "test.dump"
    parser = LAMMPSDumpParser(file_path)
    assert parser.file_path == file_path
    assert parser.data is None


def test_lammps_dump_parser_parse():
    """Test LAMMPSDumpParser parse method returns a DataFrame."""
    parser = LAMMPSDumpParser("test.dump")
    result = parser.parse()
    assert isinstance(result, pd.DataFrame)


def test_lammps_dump_parser_get_timesteps():
    """Test LAMMPSDumpParser get_timesteps method returns a list."""
    parser = LAMMPSDumpParser("test.dump")
    timesteps = parser.get_timesteps()
    assert isinstance(timesteps, list)


def test_lammps_dump_parser_get_atoms_at_timestep():
    """Test LAMMPSDumpParser get_atoms_at_timestep method returns a DataFrame."""
    parser = LAMMPSDumpParser("test.dump")
    atoms_data = parser.get_atoms_at_timestep(1000)
    assert isinstance(atoms_data, pd.DataFrame) 