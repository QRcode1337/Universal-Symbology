import unittest
import json
import os
from character_profiler import CharacterProfiler


class TestCharacterProfiler(unittest.TestCase):
    """Test suite for CharacterProfiler class."""
    
    def setUp(self):
        """Set up test fixtures."""
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
        """Test that CharacterProfiler initializes correctly."""
        profiler = CharacterProfiler(self.symbology_file)
        self.assertIsNotNone(profiler.symbology)
        self.assertIsNotNone(profiler.symbols)
        
    def test_caching_functionality(self):
        """Test that caching works correctly."""
        CharacterProfiler._symbology_cache.clear()
        CharacterProfiler._symbols_cache.clear()
        
        profiler1 = CharacterProfiler(self.symbology_file)
        self.assertIn(self.symbology_file, CharacterProfiler._symbology_cache)
        self.assertIn(self.symbology_file, CharacterProfiler._symbols_cache)
        
        profiler2 = CharacterProfiler(self.symbology_file)
        self.assertEqual(profiler1.symbology, profiler2.symbology)
        self.assertEqual(profiler1.symbols, profiler2.symbols)
        
    def test_character_profiling(self):
        """Test that character profiling works correctly."""
        profiler = CharacterProfiler(self.symbology_file)
        profile = profiler.profile_character(self.test_character)
        
        expected_keys = ['Core', 'Personality', 'Role', 'Name', 'Astrology']
        for key in expected_keys:
            self.assertIn(key, profile)
            
        self.assertIsInstance(profile['Personality'], list)
        self.assertTrue(len(profile['Personality']) > 0)
        
    def test_personality_symbol_optimization(self):
        """Test that the optimized personality symbol method works."""
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
