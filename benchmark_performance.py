import time
import json
from character_profiler import CharacterProfiler

def benchmark_original_vs_optimized():
    """Benchmark the performance improvement from caching optimization."""
    symbology_file = "textPrimer-UniversalSymbology_v01a.jsonld"
    
    CharacterProfiler._symbology_cache.clear()
    CharacterProfiler._symbols_cache.clear()
    
    example_character = {
        "Name": "TestCharacter",
        "Origin": "Celestial",
        "Role": "Mage",
        "PersonalityTraits": ["Brave", "Wise", "Mysterious"],
        "Abilities": ["Magic"],
        "Goals": ["Test"],
        "AstrologicalData": {"ZodiacSign": "Aries"},
        "NameData": {"NameMeaning": "Star"}
    }
    
    print("Performance Benchmark: CharacterProfiler Optimization")
    print("=" * 60)
    
    num_iterations = 10
    
    start_time = time.time()
    profiler1 = CharacterProfiler(symbology_file)
    first_init_time = time.time() - start_time
    
    start_time = time.time()
    profilers = []
    for i in range(num_iterations - 1):
        profilers.append(CharacterProfiler(symbology_file))
    subsequent_init_time = time.time() - start_time
    
    profile = profiler1.profile_character(example_character)
    
    print(f"First instantiation (cache miss): {first_init_time:.4f} seconds")
    print(f"Subsequent {num_iterations-1} instantiations (cache hits): {subsequent_init_time:.4f} seconds")
    print(f"Average time per cached instantiation: {subsequent_init_time/(num_iterations-1):.4f} seconds")
    print(f"Performance improvement: {first_init_time/(subsequent_init_time/(num_iterations-1)):.1f}x faster")
    
    print("\nFunctionality Test:")
    print(f"Core Symbol: {profile['Core']}")
    print(f"Personality Symbols: {profile['Personality']}")
    print(f"Role Symbol: {profile['Role']}")
    
    return first_init_time, subsequent_init_time

if __name__ == "__main__":
    benchmark_original_vs_optimized()
