import unittest
from signal_untangler import is_interweaving


class TestIsInterweaving(unittest.TestCase):
    def test_basic_examples(self):
        # Test the example from the problem statement
        self.assertTrue(is_interweaving("100010101", "101", "0"))
        
        # Simple cases
        self.assertTrue(is_interweaving("1010", "10", "10"))
        self.assertTrue(is_interweaving("1100", "10", "1"))
        self.assertFalse(is_interweaving("1110", "10", "1"))
        
    def test_empty_strings(self):
        # Empty pattern strings should return False
        self.assertFalse(is_interweaving("1010", "", "10"))
        self.assertFalse(is_interweaving("1010", "10", ""))
        self.assertFalse(is_interweaving("", "10", "01"))
        
    def test_signal_too_short(self):
        # Signal too short to contain one repetition of each pattern
        self.assertFalse(is_interweaving("10", "101", "01"))
        
    def test_discard_beginning(self):
        # Should discard characters at the beginning
        self.assertTrue(is_interweaving("11100010101", "101", "0"))
        
    def test_discard_end(self):
        # Should recognize valid interleaving even if there are extra chars at the end
        self.assertTrue(is_interweaving("10001010111", "101", "0"))
        
    def test_complex_cases(self):
        # More complex patterns
        self.assertTrue(is_interweaving("10110111011101", "101", "11111"))
        self.assertTrue(is_interweaving("100101001010", "1010", "001"))
        self.assertFalse(is_interweaving("1001010010100", "1010", "001"))  # Extra 0 at the end
        
    def test_identical_patterns(self):
        # Test with identical patterns
        self.assertTrue(is_interweaving("1010", "10", "10"))
        self.assertTrue(is_interweaving("101010", "10", "10"))
        
    def test_longer_patterns(self):
        # Test with longer patterns
        x = "10101"
        y = "110011"
        s = "1110100110011101"  # Interleaved x and y
        self.assertTrue(is_interweaving(s, x, y))


if __name__ == '__main__':
    unittest.main()
