import os
import sys
import re
import numpy as np
from typing import Optional

class dftbridge:

    def __init__(self, QEfilepath):
        self.QEfile = QEfilepath
        self.numatoms = Optional[int] = None

    """ grep-style functions that read the DFT outputs for text patterns(ATOMIC_POSITION, Total energy, Total force) and saves in list """

    def grep_numatoms(self) -> int:
        for line in open(self.QEfile, "r"):
            if re.search("number of atoms/cell", line):
                numbers = re.findall(r'\d+', line) # Extract the number from the line if the pattern was found in that line
                if numbers:
                    self.numatoms = int(numbers[0])
                    return self.numatoms  # Return the first number found, this is the number of atoms/cell in the simulation- which is how many atomic positions there will be each timestep
                
        print(f"grep failed to find number of atoms in {self.QEfile}")
        return 0
    
    def grep_atomic_positons(self) -> list:
        retstr=[]
        full_position_list = []
        timestep_x_positions = []
        postions_found = False
        for line_number, line in enumerate(open(self.QEfile, "r"), start=1):
            if re.search("ATOMIC_POSITIONS", line):
        
                for atom in self.numatoms:
                    nextline = line_number + 1 # The "ATOMIC_POSITIONS" pattern is found at line_number, so iterate line_number+1 to get the values
                    numbers = re.findall(r'-?\d+\.\d+', nextline)
                    
                    timestep_x_positions.append
                    timestep_x_positions.append()
    
    def grep_atomic_positions(self) -> list:
        poslist = []
        found_positions = False
        reading_coordinates = False

        for line in open(self.QEfile, "r"):
            if re.search("ATOMIC_POSITIONS", line): # Check if we found the ATOMIC_POSITIONS line
                found_positions = True
                reading_coordinates = True
                continue
            # for eachAtom in numatoms:
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
    
    def grep_totenergy(self) -> list:
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
            if re.search("Total force", line):
                numbers = re.findall(r'-?\d+\.\d+', line) # Extract the numbers directly from the line
                if numbers:
                    forcelist.append(float(numbers[0]))  # Take the first float found
                    foundPattern = True
        if not foundPattern:
            print(f"grep failed to find force in {self.QEfile}")
        return forcelist
    
    def grep_lattice(self) -> list:
        latlist = []
        foundPattern = False
        for line in open(self.QEfile, "r"):
            if re.search("lattice parameter", line):
                val = re.findall(r'-?\d+.\d+', line)
                if val:
                    latlist.append(float(val[0]))  # Convert first element to float
                    foundPattern = True
        if not foundPattern:
            print(f"grep failed to find lattice parameter in {self.QEfile}")
        return latlist
    
if __name__ == "__main__":
    yttrium = dftbridge("/Users/andrewtrepagnier/Forks/psuedo-lammps/tests/qe_dft_example.txt")

    print("Number of atoms:", yttrium.grep_numatoms())
    #print(np.shape(yttrium.grep_atomic_positions()))
    #print(f"The atomic positions at 9th timestep is {yttrium.grep_atomic_positions()[8]}")
    #print("Atomic positions:", yttrium.grep_atomic_positions())
    #print("Forces:", yttrium.grep_forces())
    #print("Energies:", yttrium.grep_totenergy())
    #print("Lattice parameters:", yttrium.grep_lattice())

            
