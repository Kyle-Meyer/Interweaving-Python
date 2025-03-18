import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from signal_untangler.algorithm import is_interweaving

class InterweavingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Untangler")
        self.root.geometry("600x400")
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
        
        # Button to check interweaving
        self.check_button = ttk.Button(input_frame, text="Check Interweaving", command=self.check_interweaving)
        self.check_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)
        
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
    
    def _update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for i, (s, x, y, result) in enumerate(reversed(self.history[-10:])):  # Show last 10 entries
            result_str = "✅" if result else "❌"
            self.history_text.insert(tk.END, f"{result_str} s='{s}', x='{x}', y='{y}'\n")
            
        self.history_text.config(state=tk.DISABLED)


def launch_gui():
    root = tk.Tk()
    app = InterweavingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
