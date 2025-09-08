import json


class CharacterProfiler:
    """A class to generate symbolic profiles for characters.

    This class uses a symbology file to map character traits, roles, and other
    attributes to a set of symbols. It is designed to be extensible, allowing
    for the addition of new symbols and profiling rules.

    Attributes:
        symbology (dict): The loaded symbology data from the JSON file.
        symbols (dict): A simplified dictionary of symbols extracted from the
            symbology data.
    """
    _symbology_cache = {}
    _symbols_cache = {}
    
    def __init__(self, symbology_file):
        """Initializes the CharacterProfiler with a symbology file.

        Args:
            symbology_file (str): The path to the JSON symbology file.
        """
        if symbology_file not in self._symbology_cache:
            with open(symbology_file, 'r') as f:
                self._symbology_cache[symbology_file] = json.load(f)
        
        self.symbology = self._symbology_cache[symbology_file]
        
        if symbology_file not in self._symbols_cache:
            self._symbols_cache[symbology_file] = self._extract_symbols()
        
        self.symbols = self._symbols_cache[symbology_file]

    def _find_section(self, section_name):
        """Finds a section by name in the symbology data.

        Args:
            section_name (str): The name of the section to find.

        Returns:
            dict: The section data, or None if not found.
        """
        for section in self.symbology.get("hasSection", []):
            if section.get("name") == section_name:
                return section
        return None

    def _extract_symbols(self):
        """Parses the JSON-LD structure to extract a dictionary of symbols.

        This method simplifies the complex JSON-LD structure into a more
        accessible dictionary of symbols, including elements, modalities, and
        zodiac signs.

        Returns:
            dict: A dictionary of symbols.
        """
        symbols = {"zodiac": {}}
        framework = self._find_section("Universal Symbology Framework")
        if not framework:
            return symbols

        for concept_group in framework.get("hasConcept", []):
            # Extract Elements
            if concept_group.get("@type") == "ElementGroup":
                for element in concept_group.get("hasElement", []):
                    symbols[element["name"]] = element

            # Extract Modalities
            if concept_group.get("@type") == "ModalityGroup":
                for modality in concept_group.get("hasModality", []):
                    # We store the main modality type (Cardinal, Fixed, Mutable)
                    symbols[modality["modalityType"]] = modality

            # Extract Zodiac Signs
            if concept_group.get("@type") == "AstrologicalIntegration":
                for sign in concept_group.get("hasZodiacSign", []):
                    symbols["zodiac"][sign["name"]] = sign

        # Base symbols are mentioned in multiple places, we can add them manually
        # or parse from duality groups. For now, a manual addition is simpler.
        symbols["Point"] = {"name": "Point", "description": "Existence, Origin, Singularity"}
        symbols["Line"] = {"name": "Line", "description": "Connection, Continuity, Direction"}
        symbols["Angle"] = {"name": "Angle", "description": "Intersection, Divergence, Relationship"}
        symbols["Curve"] = {"name": "Curve", "description": "Change, Fluidity, Transformation"}
        symbols["Circle"] = {"name": "Circle", "description": "Unity, Wholeness, Cycles"}
        symbols["Triangle"] = {"name": "Triangle", "description": "Stability, Harmony, Balance"}
        symbols["Square"] = {"name": "Square", "description": "Structure, Order, Foundation"}
        symbols["Spiral"] = {"name": "Spiral", "description": "Growth, Evolution, Expansion"}
        symbols["Wave"] = {"name": "Wave", "description": "Vibration, Energy, Frequency"}

        # Custom symbols from pseudocode
        symbols["SwordSymbol"] = {"name": "SwordSymbol", "description": "Symbol for a Warrior"}
        symbols["StarSymbol"] = {"name": "StarSymbol", "description": "Symbol for a Mage or Star"}
        symbols["SunSymbol"] = {"name": "SunSymbol", "description": "Symbol for Sun"}

        return symbols

    def profile_character(self, character_data):
        """Generates a symbolic profile for a character.

        This method takes a dictionary of character data and returns a symbolic
        profile based on the rules defined in the class.

        Args:
            character_data (dict): A dictionary containing character data.

        Returns:
            dict: A dictionary representing the character's symbolic profile.
        """
        core_symbol = self._determine_core_symbol(character_data)
        personality_symbols = self._determine_personality_symbols(character_data)
        role_symbol = self._determine_role_symbol(character_data)
        astrological_profile = self._determine_astrological_profile(character_data)
        name_symbol = self._determine_name_symbol(character_data)

        # Combine symbols based on grammar
        # This is a simplified representation of the final output
        profile = {
            "Core": core_symbol,
            "Personality": personality_symbols,
            "Role": role_symbol,
            "Astrology": astrological_profile,
            "Name": name_symbol,
            "Symbolic_Representation": f"Encapsulate(Superimpose({core_symbol}, {personality_symbols}), {role_symbol}) AdjacentTo({astrological_profile['Element']}, {astrological_profile['Modality']}) Enclose({name_symbol})"
        }

        return profile

    def _determine_core_symbol(self, character_data):
        """Determines the core symbol based on primary traits or origin.

        Args:
            character_data (dict): A dictionary containing character data.

        Returns:
            str: The name of the core symbol.
        """
        traits = character_data.get("PersonalityTraits", [])
        if "Brave" in traits:
            return self.symbols.get("Triangle", {}).get("name")
        if character_data.get("Origin") == "Celestial":
            return self.symbols.get("Circle", {}).get("name")
        # Default to Point for existence
        return self.symbols.get("Point", {}).get("name")

    def _determine_personality_symbols(self, character_data):
        """Determines personality symbols from a list of traits.

        Args:
            character_data (dict): A dictionary containing character data.

        Returns:
            list: A list of personality symbol names.
        """
        trait_map = {
            "Brave": "Triangle",
            "Wise": "Spiral",
            "Mysterious": "Wave",
            "Compassionate": "Circle",
            "Leader": "Angle",
        }
        traits = character_data.get("PersonalityTraits", [])
        return [trait_map[trait] for trait in traits 
                if trait in trait_map and trait_map[trait] in self.symbols]

    def _determine_role_symbol(self, character_data):
        """Determines the role symbol for the character.

        Args:
            character_data (dict): A dictionary containing character data.

        Returns:
            str: The name of the role symbol.
        """
        role_map = {
            "Warrior": "SwordSymbol",
            "Mage": "StarSymbol",
        }
        role = character_data.get("Role")
        symbol_name = role_map.get(role, "UnknownRole")
        return self.symbols.get(symbol_name, {"name": "UnknownRole"}).get("name")

    def _determine_astrological_profile(self, character_data):
        """Looks up the character's zodiac sign and returns its profile.

        The profile includes the sign's element and modality.

        Args:
            character_data (dict): A dictionary containing character data.

        Returns:
            dict: A dictionary with the astrological profile.
        """
        astro_data = character_data.get("AstrologicalData", {})
        sign_name = astro_data.get("ZodiacSign")
        if sign_name and sign_name in self.symbols["zodiac"]:
            sign_info = self.symbols["zodiac"][sign_name]
            return {
                "Sign": sign_name,
                "Element": sign_info.get("element"),
                "Modality": sign_info.get("modality")
            }
        return {
            "Sign": "Unknown",
            "Element": "Unknown",
            "Modality": "Unknown"
        }

    def _determine_name_symbol(self, character_data):
        """Determines a symbol based on the meaning of the character's name.

        Args:
            character_data (dict): A dictionary containing character data.

        Returns:
            str: The name of the symbol.
        """
        name_map = {
            "Star": "StarSymbol",
            "Sun": "SunSymbol",
        }
        name_meaning = character_data.get("NameData", {}).get("NameMeaning")
        symbol_name = name_map.get(name_meaning, "DefaultNameSymbol")
        return self.symbols.get(symbol_name, {"name": "DefaultNameSymbol"}).get("name")


if __name__ == "__main__":
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

    # 4. Print the profile in a readable format
    print("--- Character Profile for: {} ---".format(example_character["Name"]))
    print("\nCore Symbol: {}".format(character_profile["Core"]))
    print("Personality Symbols: {}".format(", ".join(character_profile["Personality"])))
    print("Role Symbol: {}".format(character_profile["Role"]))
    print("Name Symbol: {}".format(character_profile["Name"]))

    astro_profile = character_profile["Astrology"]
    print("\nAstrological Profile:")
    print("  Sign: {}".format(astro_profile["Sign"]))
    print("  Element: {}".format(astro_profile["Element"]))
    print("  Modality: {}".format(astro_profile["Modality"]))

    print("\n--- Combined Symbolic Representation ---")
    print(character_profile["Symbolic_Representation"])
    print("\n--- End of Profile ---")
