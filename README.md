# Interweaving-Python
Interweaving-Python

The algorithm determines if a signal string is an interweaving of two known repeating patterns. Here's how it works:

Initial Checks: Verify that both pattern strings are non-empty and the signal is long enough to contain at least one copy of each pattern.
Sliding Window: For each possible starting position in the signal:

Start with the initial state (0,0,false,false) representing positions in patterns x and y, and whether we've completed a full cycle of either pattern.


Process Characters: For each character from the starting position:

Try matching the current character with the next character in pattern x
Try matching with the next character in pattern y
Add all possible new states to a set


Track Pattern Completion: When we advance past the end of a pattern:

Use modulo arithmetic to wrap around to the beginning of the pattern
Set a flag indicating we've completed at least one full cycle of this pattern


Check for Success: After processing each character:

If any state shows we've completed at least one full cycle of both patterns, return true


Early Termination: If at any point we have no valid states, try the next starting position
Final Result: If we've tried all possible starting positions without finding a valid interweaving, return false

The key insight is using a state machine approach that tracks multiple possible paths simultaneously, allowing the algorithm to try all possible ways to assign each character to either pattern x or pattern y.

# Signal Untangler

A Python module for determining if a received signal is an interweaving of two known repeating patterns.

## Installation

You can install the package directly from GitHub:

```bash
pip install git+https://github.com/yourusername/signal-untangler.git
```

Or clone the repository and install it locally:

```bash
git clone https://github.com/yourusername/signal-untangler.git
cd signal-untangler
pip install -e .
```

## Usage

```python
from signal_untangler import is_interweaving

# Check if a signal is an interweaving of two patterns
result = is_interweaving("100010101", "101", "0")
print(result)  # True

# Example with patterns that don't interweave to form the signal
result = is_interweaving("1110", "10", "1")
print(result)  # False
```

## Problem Description

Given a string *s* consisting of 0s and 1s, we want to determine if it is an *interweaving* of two known repeating patterns *x* and *y*.

A string *s* is an *interweaving* of *x* and *y* if its symbols can be partitioned into two (not necessarily contiguous) subsequences *s′* and *s′′* so that:
- *s′* is a repetition of *x*
- *s′′* is a repetition of *y*
- Each symbol in *s* belongs to exactly one of *s′* or *s′′*

A string *x′* is a *repetition* of *x* if it is a prefix of *xk* for some number *k*, where *xk* denotes *k* copies of *x* concatenated together.

### Example

If *x* = 101 and *y* = 0, then *s* = 100010101 is an interweaving of *x* and *y* since:
- Characters 1,2,5,7,8,9 form 101101 – a repetition of *x*
- Characters 3,4,6 form 000 – a repetition of *y*

## Algorithm

The algorithm uses a state machine approach with the following features:
- Tries different starting positions to handle leading extraneous characters
- Tracks positions in both patterns *x* and *y* simultaneously
- Uses flags to ensure at least one complete cycle of each pattern
- Handles the repeating nature of patterns with modulo arithmetic
- Terminates early when a valid interweaving is found

Time complexity: O(|s|² × |x| × |y|) in the worst case, but typically much better in practice due to early termination.

## Testing

Run the tests using:

```bash
python -m unittest discover
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
