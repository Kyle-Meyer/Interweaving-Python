# Signal Untangler

A tool for detecting whether a received signal is an interweaving of two known repeating patterns.

## Overview

Signal Untangler is designed to solve a common problem in signal processing: determining if a received binary signal can be "untangled" into two known repeating patterns. This has applications in communication systems, particularly when monitoring signals from multiple sources.

## Algorithm Analysis

see the results under the `docs` section

### Problem Definition

Given:
- A signal string `s` consisting of 0s and 1s
- Two pattern strings `x` and `y` (also 0s and 1s)

We need to determine if `s` is an interweaving of repetitions of `x` and `y`. This means that each character in `s` can be assigned to either pattern `x` or pattern `y`, such that the characters assigned to `x` form a repetition of `x`, and the characters assigned to `y` form a repetition of `y`.

### Solution Approach

The algorithm uses a Breadth-First Search (BFS) approach to explore possible ways to match the signal with the patterns:

1. For each position in the signal `s`, we maintain:
   - Current position in pattern `x`
   - Current position in pattern `y`
   - Current position in signal `s`

2. At each step, we try matching the current character in `s` with either pattern `x` or pattern `y`.

3. If a match is found, we advance the corresponding pattern pointer (cycling back to the beginning if needed) and move to the next position in `s`.

4. We use a visited set to avoid processing the same state twice.

5. If we can process the entire string `s`, it is a valid interweaving.

### Complexity Analysis

- **Time Complexity**: O(|s| × |x| × |y|)
  - For each position in `s`, we have at most |x| × |y| different states
  - Each state is processed once due to our visited set

- **Space Complexity**: O(|s| × |x| × |y|)
  - We store states in the BFS queue and visited set
  - Maximum number of states is proportional to |s| × |x| × |y|

### Performance Characteristics

The algorithm's performance has been verified through extensive testing:
- For small inputs (signal length < 100), the algorithm typically completes in milliseconds
- For moderate inputs (signal length ~ 1000), execution time remains under 1 second
- For larger inputs (signal length > 10000), the algorithm's complexity becomes more apparent, but it still performs reasonably well

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/signal-untangler.git
   cd signal-untangler
   ```

2. Install the package:
   ```
   pip install -e .
   ```

## Usage

### Command Line Interface

Run the performance tests from the command line:

```
python -m tests.test_algorithm
```

### Graphical User Interface

Launch the GUI application:

```
python main.py
```

The GUI provides three main functionalities:

1. **Check Interweaving**:
   - Enter a signal string and two patterns
   - Click "Check Interweaving" to determine if the signal is an interweaving of the patterns

2. **Run Performance Test**:
   - Click "Run Performance Test" to execute the algorithm on a variety of test cases
   - View detailed results in the output window
   - Results are saved to the `docs` directory for future reference

3. **History Tracking**:
   - View a history of recent checks and tests

### Library Usage

You can also use the Signal Untangler as a library in your own Python code:

```python
from signal_untangler.algorithm import is_interweaving, count_comparisons

# Check if a signal is an interweaving of two patterns
result = is_interweaving("100010101", "101", "0")
print(f"Is interweaving: {result}")

# Count comparisons to measure algorithm performance
comparisons = count_comparisons("100010101", "101", "0")
print(f"Number of comparisons: {comparisons}")
```

## Project Structure

```
signal-untangler/
├── interweaving_gui/      # GUI application
│   ├── app.py             # Main GUI code
│   └── __init__.py        # Package initialization
├── signal_untangler/      # Core algorithm implementation
│   ├── algorithm.py       # Implementation of is_interweaving
│   └── __init__.py        # Package initialization
├── tests/                 # Test modules
│   ├── test_algorithm.py  # Algorithm testing functionality
│   └── __init__.py        # Package initialization
├── main.py                # Entry point for the application
├── setup.py               # Package setup file
└── README.md              # This file
```

## License

This project is licensed under the terms of the LICENSE file included in the repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
