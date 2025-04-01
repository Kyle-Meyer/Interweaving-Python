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
import io
import sys
import traceback
from contextlib import redirect_stdout

# Import the test_algorithm module
from tests.test_algorithm import test_algorithm, run_basic_tests, run_complexity_analysis

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
            
            # Capture output from test_algorithm function
            output = io.StringIO()
            with redirect_stdout(output):
                # Use the imported test_algorithm function
                test_results = test_algorithm()
            
            # Display results
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "✅ Performance tests completed!\n\n")
            self.result_text.insert(tk.END, output.getvalue())
            self.result_text.config(state=tk.DISABLED)
            
            # Update history
            self.history.append(("Performance Test", "", "", True))
            self._update_history()
            
            # Save results to file
            docs_dir = self._ensure_docs_directory()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save detailed results as JSON
            json_filename = f"{docs_dir}/performance_test_{timestamp}.json"
            with open(json_filename, 'w') as f:
                json.dump(test_results, f, indent=2)
                
            # Save raw output as text
            txt_filename = f"{docs_dir}/performance_test_output_{timestamp}.txt"
            with open(txt_filename, 'w') as f:
                f.write(output.getvalue())
                
            messagebox.showinfo("Success", f"Test results saved to:\n{txt_filename}\n{json_filename}")
            
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"❌ ERROR: {str(e)}\n\n")
            self.result_text.insert(tk.END, traceback.format_exc())
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
