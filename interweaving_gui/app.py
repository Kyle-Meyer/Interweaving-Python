import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from signal_untangler.algorithm import is_interweaving
import time
import os
import datetime
import tracemalloc
import random
import json

class InterweavingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Untangler")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Create frame for inputs
        input_frame = ttk.LabelFrame(root, text="Input Parameters")
        input_frame.pack(padx=20, pady=20, fill="x")
        
        # Signal string input
        ttk.Label(input_frame, text="Signal string (s):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.signal_entry = ttk.Entry(input_frame, width=50)
        self.signal_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.signal_entry.insert(0, "100010101")  # Default value
        
        # Pattern X input
        ttk.Label(input_frame, text="Pattern X:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.pattern_x_entry = ttk.Entry(input_frame, width=50)
        self.pattern_x_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.pattern_x_entry.insert(0, "101")  # Default value
        
        # Pattern Y input
        ttk.Label(input_frame, text="Pattern Y:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.pattern_y_entry = ttk.Entry(input_frame, width=50)
        self.pattern_y_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.pattern_y_entry.insert(0, "0")  # Default value
        
        # Button container frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=20)
        
        # Button to check interweaving
        self.check_button = ttk.Button(button_frame, text="Check Interweaving", command=self.check_interweaving)
        self.check_button.pack(side=tk.LEFT, padx=10)
        
        # Button to run performance test
        self.test_button = ttk.Button(button_frame, text="Run Performance Test", command=self.run_performance_test)
        self.test_button.pack(side=tk.LEFT, padx=10)
        
        # Result display
        result_frame = ttk.LabelFrame(root, text="Result")
        result_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.result_text = tk.Text(result_frame, height=10, width=50, wrap=tk.WORD)
        self.result_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.result_text.config(state=tk.DISABLED)
        
        # History section
        history_frame = ttk.LabelFrame(root, text="History")
        history_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.history_text = tk.Text(history_frame, height=8, width=50, wrap=tk.WORD)
        self.history_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.history_text.config(state=tk.DISABLED)
        
        # History list
        self.history = []
        
    def check_interweaving(self):
        s = self.signal_entry.get()
        x = self.pattern_x_entry.get()
        y = self.pattern_y_entry.get()
        
        if not s or not x or not y:
            messagebox.showerror("Error", "All fields must be filled out")
            return
            
        try:
            result = is_interweaving(s, x, y)
            
            # Update result display
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            
            if result:
                self.result_text.insert(tk.END, f"✅ SUCCESS: '{s}' IS an interweaving of patterns '{x}' and '{y}'")
                self.result_text.tag_add("success", "1.0", "1.end")
                self.result_text.tag_configure("success", foreground="green", font=("TkDefaultFont", 12, "bold"))
            else:
                self.result_text.insert(tk.END, f"❌ FAILURE: '{s}' is NOT an interweaving of patterns '{x}' and '{y}'")
                self.result_text.tag_add("failure", "1.0", "1.end")
                self.result_text.tag_configure("failure", foreground="red", font=("TkDefaultFont", 12, "bold"))
                
            self.result_text.config(state=tk.DISABLED)
            
            # Update history
            self.history.append((s, x, y, result))
            self._update_history()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _generate_binary_string(self, length):
        return ''.join(random.choice('01') for _ in range(length))
    
    def _ensure_docs_directory(self):
        if not os.path.exists('./docs'):
            os.makedirs('./docs')
        return './docs'
    
    def run_performance_test(self):
        try:
            # Update result display to show test is running
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Running performance tests...\n")
            self.result_text.config(state=tk.DISABLED)
            self.root.update()
            
            # Test configuration
            pattern_lengths = [2, 4, 8]  # Lengths of patterns x and y
            signal_lengths = [100, 500, 1000, 2000, 5000]  # Lengths of signal s
            results = []
            
            for x_len in pattern_lengths:
                for y_len in pattern_lengths:
                    for s_len in signal_lengths:
                        # Generate test strings
                        x = self._generate_binary_string(x_len)
                        y = self._generate_binary_string(y_len)
                        
                        # Generate a valid interweaving of x and y
                        s = self._generate_interweaving(x, y, s_len)
                        
                        # Measure time
                        start_time = time.time()
                        tracemalloc.start()
                        
                        # Run the algorithm
                        _ = is_interweaving(s, x, y)
                        
                        # Measure memory usage
                        current, peak = tracemalloc.get_traced_memory()
                        tracemalloc.stop()
                        elapsed_time = time.time() - start_time
                        
                        # Store results
                        results.append({
                            'pattern_x_length': x_len,
                            'pattern_y_length': y_len,
                            'signal_length': s_len,
                            'execution_time_ms': round(elapsed_time * 1000, 2),
                            'memory_usage_bytes': peak
                        })
            
            # Save results to file
            docs_dir = self._ensure_docs_directory()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{docs_dir}/performance_test_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': timestamp,
                    'results': results
                }, f, indent=2)
            
            # Generate summary for display
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"✅ Performance tests completed!\n\n")
            self.result_text.insert(tk.END, f"Results saved to: {filename}\n\n")
            
            # Display summary of results
            self.result_text.insert(tk.END, "Summary of Results:\n")
            for s_len in signal_lengths:
                # Calculate average time for this signal length
                times = [r['execution_time_ms'] for r in results if r['signal_length'] == s_len]
                avg_time = sum(times) / len(times) if times else 0
                self.result_text.insert(tk.END, f"Signal length {s_len}: Avg time {avg_time:.2f}ms\n")
            
            self.result_text.config(state=tk.DISABLED)
            
            # Update history
            self.history.append(("Performance Test", "", "", True))
            self._update_history()
            
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"❌ ERROR: {str(e)}")
            self.result_text.config(state=tk.DISABLED)
            messagebox.showerror("Error", f"An error occurred during testing: {str(e)}")
    
    def _generate_interweaving(self, x, y, target_length):
        result = []
        x_pos, y_pos = 0, 0
        x_len, y_len = len(x), len(y)
        
        while len(result) < target_length:
            # Randomly choose which pattern to take the next character from
            if random.random() < 0.5:
                result.append(x[x_pos])
                x_pos = (x_pos + 1) % x_len
            else:
                result.append(y[y_pos])
                y_pos = (y_pos + 1) % y_len
        
        return ''.join(result)
    
    def _update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for i, (s, x, y, result) in enumerate(reversed(self.history[-10:])):  # Show last 10 entries
            if s == "Performance Test":
                self.history_text.insert(tk.END, f"✅ Performance Test Completed\n")
            else:
                result_str = "✅" if result else "❌"
                self.history_text.insert(tk.END, f"{result_str} s='{s}', x='{x}', y='{y}'\n")
            
        self.history_text.config(state=tk.DISABLED)


def launch_gui():
    root = tk.Tk()
    app = InterweavingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
