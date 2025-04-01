# signal_untangler/__init__.py

# Directly define the functions here by importing them
from signal_untangler.algorithm import is_interweaving
from signal_untangler.algorithm import count_comparisons

# Define what gets imported with "from signal_untangler import *"
__all__ = ['is_interweaving', 'count_comparisons']
