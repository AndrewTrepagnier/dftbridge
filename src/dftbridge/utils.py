"""
Utility functions for psuedo-lammps package.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
import pandas as pd
import numpy as np


def validate_lammps_file(file_path: Union[str, Path]) -> bool:
    """
    Validate that a file appears to be a LAMMPS dump file.
    
    Args:
        file_path: Path to the file to validate.
        
    Returns:
        bool: True if file appears to be a LAMMPS dump file.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
            return first_line.startswith('ITEM: TIMESTEP')
    except:
        return False


def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary.
    
    Args:
        dictionary: The dictionary to search in.
        key: The key to look for.
        default: Default value if key is not found.
        
    Returns:
        The value associated with the key, or the default value.
    """
    return dictionary.get(key, default)


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: The directory path.
        
    Returns:
        Path: The path object for the directory.
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def list_lammps_files(directory: Union[str, Path], pattern: str = "*.dump") -> List[Path]:
    """
    List LAMMPS dump files in a directory.
    
    Args:
        directory: The directory to search in.
        pattern: The file pattern to match.
        
    Returns:
        List of Path objects for matching LAMMPS dump files.
    """
    directory_path = Path(directory)
    if not directory_path.exists():
        return []
    
    files = list(directory_path.glob(pattern))
    return [f for f in files if validate_lammps_file(f)]


def extract_box_bounds(data: pd.DataFrame) -> Dict[str, List[float]]:
    """
    Extract simulation box bounds from LAMMPS data.
    
    Args:
        data: DataFrame containing LAMMPS atom data.
        
    Returns:
        Dictionary with 'xlo', 'xhi', 'ylo', 'yhi', 'zlo', 'zhi' bounds.
    """
    # TODO: Implement box bounds extraction
    return {
        'xlo': [0.0, 0.0],
        'xhi': [0.0, 0.0],
        'ylo': [0.0, 0.0],
        'yhi': [0.0, 0.0],
        'zlo': [0.0, 0.0],
        'zhi': [0.0, 0.0],
    }


def calculate_center_of_mass(data: pd.DataFrame, mass_column: str = 'mass') -> np.ndarray:
    """
    Calculate the center of mass from atom data.
    
    Args:
        data: DataFrame containing atom positions and masses.
        mass_column: Name of the mass column.
        
    Returns:
        numpy array with [x, y, z] center of mass coordinates.
    """
    if mass_column not in data.columns:
        raise ValueError(f"Mass column '{mass_column}' not found in data")
    
    # TODO: Implement center of mass calculation
    return np.array([0.0, 0.0, 0.0]) 