# dftbridge

A lightweight, robust parser for converting Quantum Espresso DFT outputs to Large Atomic/Molecularly Massive Parallel Simulator(LAMMPS) dump files.

## Installation

```bash
pip install dftbridge
```

## Usage

```python
from dftbridge import example_function

# Use your package
result = example_function()
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AndrewTrepagnier/psuedo-lammps.git
cd psuedo-lammps
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Type Checking

```bash
mypy src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 