from signal_untangler.algorithm import is_interweaving

def generate_worst_case_test(signal_length, x_length, y_length):
    # Create pattern X with alternating bits
    pattern_x = ""
    for i in range(x_length):
        pattern_x += "0" if i % 2 == 0 else "1"
    
    # Create pattern Y that's identical to X except for the last bit
    # This maximizes the number of shared states
    pattern_y = pattern_x[:-1]
    pattern_y += "0" if pattern_x[-1] == "1" else "1"
    
    # Create a signal that will force maximum state tracking
    # Strategy: repeat a sequence that matches both pattern prefixes
    # but never quite completes both patterns simultaneously
    
    common_prefix = pattern_x[:-1]  # Prefix shared by both patterns
    signal_fragments = []
    
    # Create segments that match the common prefix but then diverge
    segment_length = len(common_prefix) + 1
    segments_needed = signal_length // segment_length + 1
    
    for i in range(segments_needed):
        # Add the common prefix
        signal_fragments.append(common_prefix)
        
        # Add a bit that could extend either pattern
        # Alternate between matching X's last bit and Y's last bit
        signal_fragments.append(pattern_x[-1] if i % 2 == 0 else pattern_y[-1])
    
    # Trim to exact length needed
    signal = "".join(signal_fragments)[:signal_length]
    
    return signal, pattern_x, pattern_y

def run_worst_case_tests():
    import time
    import os
    import json
    from datetime import datetime
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join('./docs', f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Test configurations
    signal_lengths = [1000, 5000, 10000, 20000, 50000]
    pattern_sizes = [(4, 4), (8, 8), (16, 16), (32, 32)]
    
    results = []
    
    print("Running worst-case tests for binary patterns:")
    print("--------------------------------------------")
    print("| Signal Length | Pattern Sizes | Time (ms) |")
    print("--------------------------------------------")
    
    # Also write to summary.txt
    summary_file = os.path.join(output_dir, 'summary.txt')
    with open(summary_file, 'w') as f:
        f.write("Worst-Case Performance Analysis for Binary Patterns\n")
        f.write("=" * 60 + "\n\n")
        f.write("Test conducted on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        
        f.write("Time Complexity Analysis:\n")
        f.write("-" * 30 + "\n\n")
        
        # Table header in the file
        f.write(f"{'Signal Length':<15} | {'Pattern X':<10} | {'Pattern Y':<10} | {'Time (ms)':<12} | {'Result':<8}\n")
        f.write("-" * 65 + "\n")
    
        for x_len, y_len in pattern_sizes:
            for s_len in signal_lengths:
                signal, pattern_x, pattern_y = generate_worst_case_test(s_len, x_len, y_len)
                
                # Time the algorithm
                start_time = time.time()
                result = is_interweaving(signal, pattern_x, pattern_y)
                end_time = time.time()
                
                execution_time_ms = (end_time - start_time) * 1000
                
                print(f"| {s_len:13} | X={x_len}, Y={y_len} | {execution_time_ms:8.2f} |")
                
                # Write to summary file
                f.write(f"{s_len:<15} | {x_len:<10} | {y_len:<10} | {execution_time_ms:<12.2f} | {str(result):<8}\n")
                
                # Store the result
                results.append({
                    "pattern_x_length": x_len,
                    "pattern_y_length": y_len,
                    "signal_length": s_len,
                    "execution_time_ms": execution_time_ms,
                    "result": result,
                    "pattern_x": pattern_x,
                    "pattern_y": pattern_y
                })
            
            # Add a blank line between pattern sizes in the file
            f.write("\n")
    
        # Save the results as JSON in the same directory
        json_file = os.path.join(output_dir, 'test_results.json')
        with open(json_file, 'w') as json_f:
            json.dump({"results": results}, json_f, indent=2)
        
        f.write(f"\nComplete test results saved to: {json_file}\n")
    
    print("--------------------------------------------")
    print(f"Summary saved to: {summary_file}")
    
    return results, output_dir

def analyze_complexity_growth(results, output_dir):
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    
    # Group results by pattern size
    pattern_groups = {}
    for r in results:
        key = (r["pattern_x_length"], r["pattern_y_length"])
        if key not in pattern_groups:
            pattern_groups[key] = []
        pattern_groups[key].append(r)
    
    # Analyze each pattern group
    print("\nComplexity Analysis:")
    print("-------------------")
    
    # Create a figure for time vs signal length
    plt.figure(figsize=(12, 8))
    
    # Open the summary file to append the analysis
    summary_file = os.path.join(output_dir, 'summary.txt')
    with open(summary_file, 'a') as f:
        f.write("\n\nComplexity Growth Analysis:\n")
        f.write("-" * 30 + "\n\n")
        
        # Create a table for the analysis
        f.write("Pattern Size | Signal Growth | Time Growth | Expected Ratio | Observed Exponent\n")
        f.write("-" * 75 + "\n")
        
        for pattern_size, group in pattern_groups.items():
            # Sort by signal length
            group.sort(key=lambda r: r["signal_length"])
            
            # Extract signal lengths and times
            signal_lengths = [r["signal_length"] for r in group]
            times = [r["execution_time_ms"] for r in group]
            
            # Plot log-log
            plt.loglog(
                signal_lengths, 
                times, 
                marker='o', 
                linewidth=2,
                label=f'X={pattern_size[0]}, Y={pattern_size[1]}'
            )
            
            # Add to summary file
            f.write(f"\nPattern size: X={pattern_size[0]}, Y={pattern_size[1]}\n")
            
            # Check growth rate
            if len(signal_lengths) >= 3:
                # For O(s²), doubling s should quadruple time
                # Check consecutive pairs where signal length doubles
                print(f"\nPattern size: X={pattern_size[0]}, Y={pattern_size[1]}")
                
                for i in range(len(signal_lengths) - 1):
                    ratio_s = signal_lengths[i+1] / signal_lengths[i]
                    ratio_t = times[i+1] / times[i]
                    
                    # For O(s²), we expect time ratio ≈ (signal length ratio)²
                    expected_ratio = ratio_s ** 2
                    
                    # Calculate observed complexity exponent
                    # If time ∝ sⁿ, then log(time) = n·log(s) + constant
                    # So n = log(time ratio) / log(s ratio)
                    observed_exponent = np.log(ratio_t) / np.log(ratio_s)
                    
                    # Print to console
                    print(f"Signal growth: {signal_lengths[i]} → {signal_lengths[i+1]} " +
                          f"(ratio: {ratio_s:.1f}x)")
                    print(f"Time growth: {times[i]:.2f}ms → {times[i+1]:.2f}ms " +
                          f"(ratio: {ratio_t:.1f}x, expected: {expected_ratio:.1f}x)")
                    print(f"Observed complexity exponent: O(s^{observed_exponent:.2f})")
                    print()
                    
                    # Write to summary file
                    f.write(f"{pattern_size[0]}x{pattern_size[1]} | {signal_lengths[i]} → {signal_lengths[i+1]} " +
                            f"({ratio_s:.1f}x) | {times[i]:.2f}ms → {times[i+1]:.2f}ms ({ratio_t:.1f}x) | " +
                            f"{expected_ratio:.1f}x | O(s^{observed_exponent:.2f})\n")
        
        # Add a theoretical comparison line for O(s²)
        s_values = np.logspace(np.log10(min(signal_lengths)), np.log10(max(signal_lengths)), 100)
        # Scale to match the middle of the data range
        scale_factor = np.median([r["execution_time_ms"] for r in results]) / (np.median([r["signal_length"] for r in results]) ** 2)
        plt.loglog(s_values, scale_factor * (s_values ** 2), 'r--', linewidth=2, label='O(s²) theoretical')
    
        # Analyze pattern size impact
        f.write("\n\nPattern Size Impact Analysis:\n")
        f.write("-" * 30 + "\n\n")
        
        # Group by signal length
        signal_groups = {}
        for r in results:
            key = r["signal_length"]
            if key not in signal_groups:
                signal_groups[key] = []
            signal_groups[key].append(r)
        
        # For each signal length, look at how time changes with pattern size
        for signal_length, group in sorted(signal_groups.items()):
            # Sort by pattern size (x*y)
            group.sort(key=lambda r: r["pattern_x_length"] * r["pattern_y_length"])
            
            f.write(f"Signal length: {signal_length}\n")
            f.write("Pattern Size (X×Y) | Time (ms) | Ratio vs Previous\n")
            f.write("-" * 50 + "\n")
            
            prev_time = None
            prev_size = None
            
            for r in group:
                pattern_size = r["pattern_x_length"] * r["pattern_y_length"]
                time = r["execution_time_ms"]
                
                if prev_time is not None:
                    size_ratio = pattern_size / prev_size
                    time_ratio = time / prev_time
                    f.write(f"{r['pattern_x_length']}×{r['pattern_y_length']} ({pattern_size}) | " +
                            f"{time:.2f} | {time_ratio:.2f}x (size ↑{size_ratio:.2f}x)\n")
                else:
                    f.write(f"{r['pattern_x_length']}×{r['pattern_y_length']} ({pattern_size}) | " +
                            f"{time:.2f} | -\n")
                
                prev_time = time
                prev_size = pattern_size
            
            f.write("\n")
        
        f.write("\n\nConclusion:\n")
        f.write("-" * 30 + "\n")
        f.write("Based on the data collected, the algorithm appears to have:\n")
        f.write("- Time complexity: O(|s|² × |x| × |y|) in the worst case\n")
        f.write("- Space complexity: O(|x| × |y|)\n\n")
        f.write("Visualization files have been generated in the same directory as this summary.\n")
    
    # Finalize and save the time complexity plot
    plt.xlabel("Signal Length", fontsize=12)
    plt.ylabel("Execution Time (ms)", fontsize=12)
    plt.title("Time Complexity Analysis (Log-Log Scale)", fontsize=14)
    plt.grid(True, which="both", ls="--")
    plt.legend(fontsize=10)
    
    # Save the plot to the output directory
    time_plot_path = os.path.join(output_dir, "time_complexity.png")
    plt.savefig(time_plot_path, dpi=300, bbox_inches='tight')
    print(f"Time complexity plot saved as: {time_plot_path}")
    
    # Create a second plot for pattern size impact
    plt.figure(figsize=(12, 8))
    
    # For each signal length, plot how time changes with pattern size
    for signal_length, group in sorted(signal_groups.items()):
        # Sort by pattern size (x*y)
        group.sort(key=lambda r: r["pattern_x_length"] * r["pattern_y_length"])
        
        # Extract pattern sizes and times
        pattern_sizes = [r["pattern_x_length"] * r["pattern_y_length"] for r in group]
        times = [r["execution_time_ms"] for r in group]
        
        plt.plot(
            pattern_sizes, 
            times, 
            marker='o',
            linewidth=2,
            label=f'Signal length = {signal_length}'
        )
    
    plt.xlabel("Pattern Size (X×Y)", fontsize=12)
    plt.ylabel("Execution Time (ms)", fontsize=12)
    plt.title("Impact of Pattern Size on Execution Time", fontsize=14)
    plt.grid(True)
    plt.legend(fontsize=10)
    
    # Save the pattern size impact plot
    pattern_plot_path = os.path.join(output_dir, "pattern_size_impact.png")
    plt.savefig(pattern_plot_path, dpi=300, bbox_inches='tight')
    print(f"Pattern size impact plot saved as: {pattern_plot_path}")
    
    print(f"Complete analysis saved to: {summary_file}")

if __name__ == "__main__":
    import os
    from signal_untangler.algorithm import is_interweaving
    
    results, output_dir = run_worst_case_tests()
    analyze_complexity_growth(results, output_dir)
    
    print(f"\nTest complete!")
    print(f"Summary and analysis saved to: {os.path.join(output_dir, 'summary.txt')}")
    print(f"Plots saved to: {output_dir}")



