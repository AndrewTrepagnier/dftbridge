import os
import sys
import re


class dftbridge:
    def __init__(self, QEfilepath):
        self.QEfile = QEfilepath

    def grep_atomic_positions(self) -> list[float]:
        """Robust Unix grep-style function that reads and extracts atomic positon data from QE DFT outputs"""
        poslist = []
        found_positions = False
        reading_coordinates = False

        for line in open(self.QEfilepath, "r"):
            if re.search("ATOMIC_POSITIONS", line): # Check if we found the ATOMIC_POSITIONS line
                found_positions = True
                reading_coordinates = True
                continue
            if reading_coordinates and line.strip(): # If we're reading coordinates, extract numbers from the line
                tau_match = re.search(r'tau\(\s*([^)]+)\)', line) # Look specifically for numbers inside tau(...)
                if tau_match:
                    tau_content = tau_match.group(1)
                    
                    numbers = re.findall(r'-?\d+\.\d+', tau_content)
                    if len(numbers) >= 3:
                        coords = [float(num) for num in numbers[:3]] 
                        poslist.append(coords)
                elif not line.strip().startswith('!'):
                    reading_coordinates = False

        if not found_positions:
            print(f"grep failed to find ATOMIC_POSITIONS in {self.QEfile}")
    
        return poslist
    
    def grep_totenergy(self) -> list[float]:
        energylist = []
        foundPattern = False
        for line in open(self.QEfile, "r"):
            
            if line.startswith("!") and re.search("total energy", line):
                numbers = re.findall(r'-?\d+\.\d+', line)
                if numbers:
                    energylist.append(float(numbers[0]))  # Take the first float found
                    foundPattern = True
        if not foundPattern:
            print(f"grep failed to find energies in {self.QEfile}")
        return energylist

    def grep_forces(self) -> list:
        forcelist = []
        foundPattern = False
        for line in open(self.QEfile, "r"):
            if re.search("force", line):
                forcelist.append(line)
            if not foundPattern:
                print(f"grep failed to find force in {self.QEfile}")
        return forcelist
    