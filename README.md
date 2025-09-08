# Universal Symbology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13750459.svg)](https://doi.org/10.5281/zenodo.13750459)

This repository provides a Python-based framework for Universal Symbology, a system for generating symbolic representations of characters based on their traits, origins, and other attributes.

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jthora/Universal-Symbology.git
   ```
2. Navigate to the repository directory:
   ```bash
   cd Universal-Symbology
   ```

## Usage

The core of this repository is the `CharacterProfiler` class, which is used to generate symbolic profiles for characters.

To use the `CharacterProfiler`, you need a symbology file in JSON-LD format. An example file, `textPrimer-UniversalSymbology_v01a.jsonld`, is provided in this repository.

Here's an example of how to use the `CharacterProfiler`:

```python
from character_profiler import CharacterProfiler

# 1. Create an instance of the profiler
profiler = CharacterProfiler("textPrimer-UniversalSymbology_v01a.jsonld")

# 2. Define an example character
example_character = {
    "Name": "Astra",
    "Origin": "Celestial",
    "Role": "Mage",
    "PersonalityTraits": ["Brave", "Wise", "Mysterious"],
    "Abilities": ["Starlight Magic", "Prophecy"],
    "Goals": ["Uncover the secrets of the cosmos"],
    "AstrologicalData": {
        "ZodiacSign": "Aries"
    },
    "NameData": {
        "NameMeaning": "Star"
    }
}

# 3. Generate the profile
character_profile = profiler.profile_character(example_character)

# 4. Print the profile
print(character_profile)
```

## Testing

This repository uses Python's built-in `unittest` module for testing. To run the tests, execute the following command from the root of the repository:

```bash
python3 -m unittest test_character_profiler.py
```

## Benchmarking

A benchmark script is included to demonstrate the performance benefits of caching the symbology file. To run the benchmark, execute the following command:

```bash
python3 benchmark_performance.py
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
