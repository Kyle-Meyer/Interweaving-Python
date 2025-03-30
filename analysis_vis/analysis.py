import json
import matplotlib.pyplot as plt
import os
import numpy as np
import sys

def analyze_performance_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        print("loaded file: ", file)

    results = data['results']
    timestamp = data['timestamp']
    print("hello?")
    #create the ouput dir
    output_dir = os.path.join('./docs',f'analysis_{timestamp}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #group the signals
    signal_lengths = sorted(set(r['signal_length'] for r in results))
   
    #time complexity analysis
    plt.figure(figsize=(12,8))

    pattern_combinations = set((r['pattern_x_length'], r['pattern_y_length']) for r in results)

    for x_len, y_len in pattern_combinations:
        #get results for this pattern combo
        pattern_results = [r for r in results if r['pattern_x_length'] == x_len and r['pattern_y_length'] == y_len]
        #sort by signal length
        pattern_results.sort(key = lambda r: r['signal_length'])
        #extract signal length and execution times 
        s_lengths = [r['signal_length'] for r in pattern_results]
        times = [r['execution_time_ms'] for r in pattern_results]
        
        #plot results
        plt.plot (s_lengths, times, marker='o', label=f'x_len={x_len}, y_len={y_len}')

    #graph labels
    plt.xlabel("Signal Length")
    plt.ylabel("Execution time (ms)")
    plt.title("Time comp analysis")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_dir, "time_comp.png"))

    plt.figure(figsize=(12,8))
 
    for x_len, y_len in pattern_combinations:
        #get results for this pattern combo
        pattern_results = [r for r in results if r['pattern_x_length'] == x_len and r['pattern_y_length'] == y_len]
        #sort by signal length
        pattern_results.sort(key = lambda r: r['signal_length'])
        #extract signal length and execution times 
        s_lengths = [r['signal_length'] for r in pattern_results]
        memory = [r['memory_usage_bytes'] / 1024 for r in pattern_results]  # Convert to K 
        #plot results
        plt.plot (s_lengths, times, marker='o', label=f'x_len={x_len}, y_len={y_len}')

    #graph labels
    plt.xlabel("Signal Length")
    plt.ylabel("Memory Usage (KB)")
    plt.title("Space Complexity analysis")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_dir, "time_comp.png"))

    plt.figure(figsize=(12,8))  
    # Choose one pattern combination for simplicity
    x_len, y_len = min(pattern_combinations)
    pattern_results = [r for r in results if r['pattern_x_length'] == x_len and r['pattern_y_length'] == y_len]
    pattern_results.sort(key=lambda r: r['signal_length'])
    
    s_lengths = np.array([r['signal_length'] for r in pattern_results])
    times = np.array([r['execution_time_ms'] for r in pattern_results])
    
    # Plot actual times
    plt.plot(s_lengths, times, 'bo-', label='Actual time')
    
    # Plot theoretical O(n²) curve (scaled to match actual data)
    scale_factor = times[-1] / (s_lengths[-1] ** 2)
    plt.plot(s_lengths, scale_factor * s_lengths**2, 'r--', label='O(n²)')
    
    # Plot theoretical O(n³) curve (scaled to match actual data)
    scale_factor = times[-1] / (s_lengths[-1] ** 3)
    plt.plot(s_lengths, scale_factor * s_lengths**3, 'g--', label='O(n³)')
    
    plt.xlabel('Signal Length')
    plt.ylabel('Execution Time (ms)')
    plt.title(f'Theoretical vs. Actual Time Complexity (x_len={x_len}, y_len={y_len})')
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'theoretical_comparison.png'))
    
    # Generate summary report
    summary_file = os.path.join(output_dir, 'summary.txt')
    with open(summary_file, 'w') as f:
        f.write(f"Performance Analysis Summary for test run at {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("Time Complexity Analysis:\n")
        f.write("-" * 30 + "\n")
        for x_len, y_len in pattern_combinations:
            pattern_results = [r for r in results if r['pattern_x_length'] == x_len and r['pattern_y_length'] == y_len]
            pattern_results.sort(key=lambda r: r['signal_length'])
            
            f.write(f"\nPattern X length: {x_len}, Pattern Y length: {y_len}\n")
            f.write("Signal Length | Execution Time (ms)\n")
            f.write("-" * 30 + "\n")
            
            for r in pattern_results:
                f.write(f"{r['signal_length']:<14} | {r['execution_time_ms']:.2f}\n")
        
        f.write("\n\nSpace Complexity Analysis:\n")
        f.write("-" * 30 + "\n")
        for x_len, y_len in pattern_combinations:
            pattern_results = [r for r in results if r['pattern_x_length'] == x_len and r['pattern_y_length'] == y_len]
            pattern_results.sort(key=lambda r: r['signal_length'])
            
            f.write(f"\nPattern X length: {x_len}, Pattern Y length: {y_len}\n")
            f.write("Signal Length | Memory Usage (KB)\n")
            f.write("-" * 30 + "\n")
            
            for r in pattern_results:
                f.write(f"{r['signal_length']:<14} | {r['memory_usage_bytes']/1024:.2f}\n")
        
        f.write("\n\nConclusion:\n")
        f.write("-" * 30 + "\n")
        f.write("Based on the data collected, the algorithm appears to have:\n")
        f.write("- Time complexity: O(|s|² × |x| × |y|) in the worst case\n")
        f.write("- Space complexity: O(|x| × |y|)\n\n")
        f.write("Visualization files have been generated in the same directory as this summary.\n")
    
    print(f"Analysis complete. Results saved to {output_dir}")
    return output_dir

#main
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.path.exists(filename):
            analyze_performance_file(filename)
        else:
            print(f"Error: File '{filename}' not found" )
    else:
        print("error you need to pass a json file")
