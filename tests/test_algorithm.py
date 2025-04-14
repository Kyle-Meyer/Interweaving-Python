import time
from signal_untangler.algorithm import is_interweaving, count_comparisons

def get_test_cases():
    return [
        # s, x, y, expected_result
        ("100010101", "101", "0", True),      # Example from problem statement
        ("1010", "10", "1", True),           # Simple example
        ("0101", "01", "10", True),         # Not an interweaving, but technically true because X alone is the repeating
        ("1100110011", "11", "00", True),    # Alternating patterns
        ("01010101", "01", "01", True),      # Same pattern
        ("", "0", "1", False),               # Empty s
        ("0", "", "1", False),               # Empty x
        ("1", "0", "", False),               # Empty y
        ("01234", "01", "23", False),        # Invalid characters
    ]

def run_basic_tests():
    results = []
    test_cases = get_test_cases()
    
    print("Testing algorithm...")
    print("=" * 50)
    for i, (s, x, y, expected) in enumerate(test_cases):
        result = is_interweaving(s, x, y)
        comparisons = count_comparisons(s, x, y)
        
        test_result = {
            "test_id": i + 1,
            "signal": s,
            "pattern_x": x,
            "pattern_y": y,
            "expected": expected,
            "result": result,
            "comparisons": comparisons,
            "success": result == expected
        }
        results.append(test_result)
        
        print(f"Test {i+1}:")
        print(f"s = {s}, x = {x}, y = {y}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"Comparisons: {comparisons}")
        print("-" * 50)
    
    return results

def generate_interweaved_string(x_pattern, y_pattern, length):
    s = ""
    x_counter = 0
    y_counter = 0
    
    for i in range(length):
        if i % 2 == 0 and i % 3 != 0:
            s += x_pattern[x_counter % len(x_pattern)]
            x_counter += 1
        else:
            s += y_pattern[y_counter % len(y_pattern)]
            y_counter += 1
    
    return s

def run_complexity_analysis(lengths=None, x_pattern="101", y_pattern="0"):
    if lengths is None:
        lengths = [10, 100, 1000, 5000]
    
    results = []
    
    print("\nComplexity Analysis:")
    print("=" * 50)
    print(f"Using fixed patterns x = {x_pattern}, y = {y_pattern}")
    print(f"{'Length of s':<15}{'Comparisons':<15}{'Time (s)':<15}")
    print("-" * 45)
    
    for length in lengths:
        # Create test signal - interweaving of x and y
        s = generate_interweaved_string(x_pattern, y_pattern, length)
        
        # Measure performance
        start_time = time.time()
        comparisons = count_comparisons(s, x_pattern, y_pattern)
        elapsed_time = time.time() - start_time
        
        result = {
            "length": length,
            "comparisons": comparisons,
            "time_seconds": elapsed_time
        }
        results.append(result)
        
        print(f"{length:<15}{comparisons:<15}{elapsed_time:<15.6f}")
    
    return results

def test_algorithm():
    basic_results = run_basic_tests()
    complexity_results = run_complexity_analysis()
    
    return {
        "basic_tests": basic_results,
        "complexity_analysis": complexity_results
    }

# Run tests if script is executed directly
if __name__ == "__main__":
    test_algorithm()
