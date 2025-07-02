"""
Base class for DFT output extractors.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import json
import pandas as pd
import numpy as np


class BaseExtractor(ABC):
    """
    Abstract base class for extracting data from DFT output files.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the extractor.
        
        Args:
            file_path: Path to the DFT output file
        """
        self.file_path = file_path
        self.lines = []
        self.metadata = {}
        self.system_info = {}
        
        # Common elements for LAMMPS conversion
        self.common_elements = {
            'H': {'number': 1, 'mass': 1.008},
            'C': {'number': 6, 'mass': 12.011},
            'N': {'number': 7, 'mass': 14.007},
            'O': {'number': 8, 'mass': 15.999},
            'Si': {'number': 14, 'mass': 28.085},
            'S': {'number': 16, 'mass': 32.065},
            'Fe': {'number': 26, 'mass': 55.845},
            'Cu': {'number': 29, 'mass': 63.546},
            'Au': {'number': 79, 'mass': 196.967},
            'Al': {'number': 13, 'mass': 26.982},
            'Ti': {'number': 22, 'mass': 47.867},
            'Mo': {'number': 42, 'mass': 95.94},
            'W': {'number': 74, 'mass': 183.84}
        }
    
    def read_file(self):
        """Read the entire file into memory."""
        with open(self.file_path, 'r') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.lines = self.remove_comments(self.lines)
    
    def remove_comments(self, lines: List[str], comment_char: str = '#') -> List[str]:
        """Remove comments from input lines."""
        clean_lines = []
        for line in lines:
            partitioned = line.lstrip().partition(comment_char)
            if partitioned[0] != "":
                clean_lines.append(partitioned[0])
        return clean_lines
    
    def find_section(self, pattern: str) -> List[str]:
        """Find lines matching a pattern."""
        import re
        matches = []
        for line in self.lines:
            if re.search(pattern, line):
                matches.append(line)
        return matches
    
    @abstractmethod
    def extract_coordinates(self) -> pd.DataFrame:
        """Extract atomic coordinates."""
        pass
    
    @abstractmethod
    def extract_lattice(self) -> np.ndarray:
        """Extract lattice vectors."""
        pass
    
    @abstractmethod
    def extract_energies(self) -> Dict[str, float]:
        """Extract energy information."""
        pass
    
    def extract_system_info(self) -> Dict[str, Any]:
        """Extract general system information."""
        return {
            'calculation_type': self.get_calculation_type(),
            'number_of_atoms': len(self.extract_coordinates()),
            'elements_present': list(self.extract_coordinates()['element'].unique()),
            'lattice_volume': np.linalg.det(self.extract_lattice())
        }
    
    @abstractmethod
    def get_calculation_type(self) -> str:
        """Return the type of calculation."""
        pass
    
    def save_metadata(self, output_path: str):
        """Save metadata and system information to JSON file."""
        data = {
            'metadata': self.metadata,
            'system_info': self.system_info,
            'calculation_type': self.get_calculation_type(),
            'file_path': self.file_path
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def extract_all(self) -> Dict[str, Any]:
        """Extract all available data from the file."""
        self.read_file()
        
        coordinates = self.extract_coordinates()
        lattice = self.extract_lattice()
        energies = self.extract_energies()
        system_info = self.extract_system_info()
        
        return {
            'coordinates': coordinates,
            'lattice': lattice,
            'energies': energies,
            'system_info': system_info,
            'metadata': self.metadata
        } 