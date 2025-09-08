import unittest
import json
import os
from character_profiler import CharacterProfiler


class TestCharacterProfiler(unittest.TestCase):
    """Test suite for the CharacterProfiler class.

    This class contains a series of tests to ensure that the
    CharacterProfiler class functions as expected. It covers
    initialization, caching, and the profiling process itself.
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.symbology_file = "textPrimer-UniversalSymbology_v01a.jsonld"
        self.test_character = {
            "Name": "TestCharacter",
            "Origin": "Celestial",
            "Role": "Mage",
            "PersonalityTraits": ["Brave", "Wise", "Mysterious"],
            "Abilities": ["Magic"],
            "Goals": ["Test"],
            "AstrologicalData": {"ZodiacSign": "Aries"},
            "NameData": {"NameMeaning": "Star"}
        }
        
    def test_profiler_initialization(self):
        """Test that the CharacterProfiler initializes correctly.

        Ensures that the symbology and symbols attributes are loaded
        and are not None.
        """
        profiler = CharacterProfiler(self.symbology_file)
        self.assertIsNotNone(profiler.symbology)
        self.assertIsNotNone(profiler.symbols)
        
    def test_caching_functionality(self):
        """Test that the caching mechanism works as expected.

        Verifies that the symbology and symbols data are cached after the
        first instantiation and that subsequent instantiations use the
        cached data.
        """
        CharacterProfiler._symbology_cache.clear()
        CharacterProfiler._symbols_cache.clear()
        
        profiler1 = CharacterProfiler(self.symbology_file)
        self.assertIn(self.symbology_file, CharacterProfiler._symbology_cache)
        self.assertIn(self.symbology_file, CharacterProfiler._symbols_cache)
        
        profiler2 = CharacterProfiler(self.symbology_file)
        self.assertEqual(profiler1.symbology, profiler2.symbology)
        self.assertEqual(profiler1.symbols, profiler2.symbols)
        
    def test_character_profiling(self):
        """Test the overall character profiling process.

        Ensures that the profile_character method returns a dictionary
        with the expected keys and that the data types are correct.
        """
        profiler = CharacterProfiler(self.symbology_file)
        profile = profiler.profile_character(self.test_character)
        
        expected_keys = ['Core', 'Personality', 'Role', 'Name', 'Astrology']
        for key in expected_keys:
            self.assertIn(key, profile)
            
        self.assertIsInstance(profile['Personality'], list)
        self.assertTrue(len(profile['Personality']) > 0)
        
    def test_personality_symbol_determination(self):
        """Test the determination of personality symbols.

        Verifies that the _determine_personality_symbols method correctly
        maps personality traits to symbols and handles various edge cases,
        such as empty or invalid trait lists.
        """
        profiler = CharacterProfiler(self.symbology_file)
        
        character_data = {"PersonalityTraits": ["Brave", "Wise"]}
        symbols = profiler._determine_personality_symbols(character_data)
        
        self.assertIsInstance(symbols, list)
        
        character_data = {"PersonalityTraits": []}
        symbols = profiler._determine_personality_symbols(character_data)
        self.assertEqual(symbols, [])
        
        character_data = {"PersonalityTraits": ["InvalidTrait"]}
        symbols = profiler._determine_personality_symbols(character_data)
        self.assertEqual(symbols, [])


if __name__ == '__main__':
    unittest.main()
