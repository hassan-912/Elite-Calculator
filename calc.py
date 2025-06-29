import customtkinter as ctk
from tkinter import messagebox, filedialog
import math
import datetime
import json
import os
from typing import Dict, List, Any

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class AdvancedCalculator:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🧮 Elite Calculator")
        self.window.geometry("400x600")
        self.window.resizable(True, True)
        
        # Color scheme
        self.colors = {
            "bg_primary": "#0a0a0a",
            "bg_secondary": "#1a1a1a", 
            "bg_tertiary": "#2a2a2a",
            "accent_blue": "#00d4ff",
            "accent_purple": "#8b5cf6",
            "accent_green": "#10b981",
            "accent_orange": "#f59e0b",
            "accent_red": "#ef4444",
            "text_primary": "#ffffff",
            "text_secondary": "#a1a1aa"
        }
        
        # Calculator state
        self.current_expression = ""
        self.display_var = ctk.StringVar(value="0")
        self.memory = 0
        self.history = []
        self.current_mode = "Standard"
        self.angle_mode = "DEG"  # DEG, RAD, GRAD
        
        # Variables for programming mode
        self.current_base = "DEC"  # DEC, HEX, OCT, BIN
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.window.configure(fg_color=self.colors["bg_primary"])
        
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["bg_secondary"],
            corner_radius=20,
            border_width=2,
            border_color=self.colors["accent_blue"]
        )
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mode selector
        self.create_mode_selector(main_frame)
        
        # Display area
        self.create_display_area(main_frame)
        
        # Button area (will change based on mode)
        self.button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create initial standard mode
        self.switch_mode("Standard")
        
    def create_mode_selector(self, parent):
        mode_frame = ctk.CTkFrame(parent, fg_color="transparent")
        mode_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        modes = ["Standard", "Scientific", "Programming", "Date", "Converter"]
        for i, mode in enumerate(modes):
            btn = ctk.CTkButton(
                mode_frame,
                text=mode,
                width=70,
                height=30,
                font=ctk.CTkFont(size=10),
                command=lambda m=mode: self.switch_mode(m),
                fg_color=self.colors["accent_purple"] if mode == self.current_mode else self.colors["bg_tertiary"]
            )
            btn.grid(row=0, column=i, padx=2, pady=2)
            
        # Configure grid
        for i in range(len(modes)):
            mode_frame.grid_columnconfigure(i, weight=1)
    
    def create_display_area(self, parent):
        display_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.colors["accent_purple"]
        )
        display_frame.pack(fill="x", padx=10, pady=5)
        
        # Mode and angle indicator
        info_frame = ctk.CTkFrame(display_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        self.mode_label = ctk.CTkLabel(
            info_frame,
            text=f"{self.current_mode} | {self.angle_mode}",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_secondary"]
        )
        self.mode_label.pack(side="left")
        
        self.memory_indicator = ctk.CTkLabel(
            info_frame,
            text="M" if self.memory != 0 else "",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors["accent_orange"]
        )
        self.memory_indicator.pack(side="right")
        
        # Expression display
        self.expression_display = ctk.CTkLabel(
            display_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"],
            anchor="e"
        )
        self.expression_display.pack(fill="x", padx=10)
        
        # Main display
        self.display = ctk.CTkEntry(
            display_frame,
            textvariable=self.display_var,
            font=ctk.CTkFont(size=24, weight="bold"),
            height=60,
            justify="right",
            state="readonly",
            fg_color="transparent",
            border_width=0,
            text_color=self.colors["text_primary"]
        )
        self.display.pack(fill="x", padx=10, pady=(0, 10))
    
    def switch_mode(self, mode):
        self.current_mode = mode
        
        # Clear button frame
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Update mode label
        self.mode_label.configure(text=f"{self.current_mode} | {self.angle_mode}")
        
        # Create appropriate button layout
        if mode == "Standard":
            self.create_standard_buttons()
        elif mode == "Scientific":
            self.create_scientific_buttons()
        elif mode == "Programming":
            self.create_programming_buttons()
        elif mode == "Date":
            self.create_date_calculator()
        elif mode == "Converter":
            self.create_converter()
    
    def create_standard_buttons(self):
        # Memory buttons row
        memory_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        memory_frame.pack(fill="x", pady=(0, 5))
        
        memory_buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("MS", self.memory_store)
        ]
        
        for i, (text, cmd) in enumerate(memory_buttons):
            btn = ctk.CTkButton(
                memory_frame,
                text=text,
                width=60,
                height=35,
                font=ctk.CTkFont(size=12),
                command=cmd,
                fg_color=self.colors["accent_purple"],
                hover_color="#a855f7"
            )
            btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
        
        for i in range(5):
            memory_frame.grid_columnconfigure(i, weight=1)
        
        # Main calculator grid
        calc_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        calc_frame.pack(fill="both", expand=True)
        
        # Standard calculator layout
        buttons = [
            [("CE", self.clear_entry), ("C", self.clear), ("⌫", self.backspace), ("÷", lambda: self.add_to_expression("/"))],
            [("7", lambda: self.add_to_expression("7")), ("8", lambda: self.add_to_expression("8")), ("9", lambda: self.add_to_expression("9")), ("×", lambda: self.add_to_expression("*"))],
            [("4", lambda: self.add_to_expression("4")), ("5", lambda: self.add_to_expression("5")), ("6", lambda: self.add_to_expression("6")), ("−", lambda: self.add_to_expression("-"))],
            [("1", lambda: self.add_to_expression("1")), ("2", lambda: self.add_to_expression("2")), ("3", lambda: self.add_to_expression("3")), ("+", lambda: self.add_to_expression("+"))],
            [("±", self.toggle_sign), ("0", lambda: self.add_to_expression("0")), (".", lambda: self.add_to_expression(".")), ("=", self.calculate)]
        ]
        
        for row, button_row in enumerate(buttons):
            for col, (text, cmd) in enumerate(button_row):
                self.create_calc_button(calc_frame, text, row, col, cmd)
        
        # Configure grid
        for i in range(5):
            calc_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            calc_frame.grid_columnconfigure(i, weight=1)
    
    def create_scientific_buttons(self):
        # Angle mode selector
        angle_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        angle_frame.pack(fill="x", pady=(0, 5))
        
        for i, mode in enumerate(["DEG", "RAD", "GRAD"]):
            btn = ctk.CTkButton(
                angle_frame,
                text=mode,
                width=60,
                height=30,
                font=ctk.CTkFont(size=10),
                command=lambda m=mode: self.set_angle_mode(m),
                fg_color=self.colors["accent_green"] if mode == self.angle_mode else self.colors["bg_tertiary"]
            )
            btn.grid(row=0, column=i, padx=2, pady=2)
        
        for i in range(3):
            angle_frame.grid_columnconfigure(i, weight=1)
        
        # Scientific functions
        sci_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        sci_frame.pack(fill="both", expand=True)
        
        # Extended scientific layout
        buttons = [
            [("sin", lambda: self.add_function("sin")), ("cos", lambda: self.add_function("cos")), ("tan", lambda: self.add_function("tan")), ("ln", lambda: self.add_function("log"))],
            [("asin", lambda: self.add_function("asin")), ("acos", lambda: self.add_function("acos")), ("atan", lambda: self.add_function("atan")), ("log", lambda: self.add_function("log10"))],
            [("π", lambda: self.add_to_expression("math.pi")), ("e", lambda: self.add_to_expression("math.e")), ("x²", lambda: self.add_to_expression("**2")), ("√", lambda: self.add_function("sqrt"))],
            [("x^y", lambda: self.add_to_expression("**")), ("1/x", self.reciprocal), ("n!", self.factorial), ("(", lambda: self.add_to_expression("("))],
            [("7", lambda: self.add_to_expression("7")), ("8", lambda: self.add_to_expression("8")), ("9", lambda: self.add_to_expression("9")), (")", lambda: self.add_to_expression(")"))],
            [("4", lambda: self.add_to_expression("4")), ("5", lambda: self.add_to_expression("5")), ("6", lambda: self.add_to_expression("6")), ("÷", lambda: self.add_to_expression("/"))],
            [("1", lambda: self.add_to_expression("1")), ("2", lambda: self.add_to_expression("2")), ("3", lambda: self.add_to_expression("3")), ("×", lambda: self.add_to_expression("*"))],
            [("0", lambda: self.add_to_expression("0")), (".", lambda: self.add_to_expression(".")), ("=", self.calculate), ("+", lambda: self.add_to_expression("+"))]
        ]
        
        for row, button_row in enumerate(buttons):
            for col, (text, cmd) in enumerate(button_row):
                self.create_calc_button(sci_frame, text, row, col, cmd)
        
        # Configure grid
        for i in range(len(buttons)):
            sci_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            sci_frame.grid_columnconfigure(i, weight=1)
    
    def create_programming_buttons(self):
        # Base selector
        base_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        base_frame.pack(fill="x", pady=(0, 5))
        
        for i, base in enumerate(["DEC", "HEX", "OCT", "BIN"]):
            btn = ctk.CTkButton(
                base_frame,
                text=base,
                width=60,
                height=30,
                font=ctk.CTkFont(size=10),
                command=lambda b=base: self.set_base_mode(b),
                fg_color=self.colors["accent_orange"] if base == self.current_base else self.colors["bg_tertiary"]
            )
            btn.grid(row=0, column=i, padx=2, pady=2)
        
        for i in range(4):
            base_frame.grid_columnconfigure(i, weight=1)
        
        # Programming calculator layout
        prog_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        prog_frame.pack(fill="both", expand=True)
        
        # Add programming-specific buttons
        buttons = [
            [("AND", lambda: self.add_to_expression(" & ")), ("OR", lambda: self.add_to_expression(" | ")), ("XOR", lambda: self.add_to_expression(" ^ ")), ("NOT", lambda: self.add_to_expression("~"))],
            [("<<", lambda: self.add_to_expression(" << ")), (">>", lambda: self.add_to_expression(" >> ")), ("MOD", lambda: self.add_to_expression(" % ")), ("C", self.clear)],
            [("A", lambda: self.add_hex_digit("A")), ("B", lambda: self.add_hex_digit("B")), ("C", lambda: self.add_hex_digit("C")), ("D", lambda: self.add_hex_digit("D"))],
            [("E", lambda: self.add_hex_digit("E")), ("F", lambda: self.add_hex_digit("F")), ("(", lambda: self.add_to_expression("(")), (")", lambda: self.add_to_expression(")"))],
            [("7", lambda: self.add_to_expression("7")), ("8", lambda: self.add_to_expression("8")), ("9", lambda: self.add_to_expression("9")), ("÷", lambda: self.add_to_expression("/"))],
            [("4", lambda: self.add_to_expression("4")), ("5", lambda: self.add_to_expression("5")), ("6", lambda: self.add_to_expression("6")), ("×", lambda: self.add_to_expression("*"))],
            [("1", lambda: self.add_to_expression("1")), ("2", lambda: self.add_to_expression("2")), ("3", lambda: self.add_to_expression("3")), ("−", lambda: self.add_to_expression("-"))],
            [("0", lambda: self.add_to_expression("0")), (".", lambda: self.add_to_expression(".")), ("=", self.calculate), ("+", lambda: self.add_to_expression("+"))]
        ]
        
        for row, button_row in enumerate(buttons):
            for col, (text, cmd) in enumerate(button_row):
                self.create_calc_button(prog_frame, text, row, col, cmd)
        
        # Configure grid
        for i in range(len(buttons)):
            prog_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            prog_frame.grid_columnconfigure(i, weight=1)
    
    def create_date_calculator(self):
        # Date calculation interface
        date_frame = ctk.CTkFrame(self.button_frame, fg_color=self.colors["bg_tertiary"])
        date_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(date_frame, text="Date Calculator", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Date inputs
        ctk.CTkLabel(date_frame, text="From Date (YYYY-MM-DD):").pack()
        self.date1_entry = ctk.CTkEntry(date_frame, placeholder_text="2025-01-01")
        self.date1_entry.pack(pady=5)
        
        ctk.CTkLabel(date_frame, text="To Date (YYYY-MM-DD):").pack()
        self.date2_entry = ctk.CTkEntry(date_frame, placeholder_text="2025-12-31")
        self.date2_entry.pack(pady=5)
        
        ctk.CTkButton(date_frame, text="Calculate Difference", command=self.calculate_date_difference).pack(pady=10)
        
        self.date_result = ctk.CTkLabel(date_frame, text="", wraplength=300)
        self.date_result.pack(pady=10)
    
    def create_converter(self):
        # Unit converter interface
        conv_frame = ctk.CTkFrame(self.button_frame, fg_color=self.colors["bg_tertiary"])
        conv_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(conv_frame, text="Unit Converter", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Conversion type selector
        self.conv_type = ctk.CTkOptionMenu(conv_frame, values=["Length", "Weight", "Temperature", "Volume"])
        self.conv_type.pack(pady=5)
        
        # Input
        self.conv_input = ctk.CTkEntry(conv_frame, placeholder_text="Enter value")
        self.conv_input.pack(pady=5)
        
        # From and To units
        self.from_unit = ctk.CTkOptionMenu(conv_frame, values=["meter", "kilometer", "centimeter", "inch", "foot"])
        self.from_unit.pack(pady=5)
        
        self.to_unit = ctk.CTkOptionMenu(conv_frame, values=["meter", "kilometer", "centimeter", "inch", "foot"])
        self.to_unit.pack(pady=5)
        
        ctk.CTkButton(conv_frame, text="Convert", command=self.convert_units).pack(pady=10)
        
        self.conv_result = ctk.CTkLabel(conv_frame, text="")
        self.conv_result.pack(pady=10)
    
    def create_calc_button(self, parent, text, row, col, command):
        # Determine button style based on text
        if text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            style = "number"
        elif text in ["+", "−", "×", "÷", "="]:
            style = "operator"
        elif text in ["C", "CE", "⌫"]:
            style = "clear"
        else:
            style = "function"
        
        colors = {
            "number": {"fg": self.colors["bg_tertiary"], "hover": self.colors["accent_blue"]},
            "operator": {"fg": self.colors["accent_orange"], "hover": "#fbbf24"},
            "clear": {"fg": self.colors["accent_red"], "hover": "#f87171"},
            "function": {"fg": self.colors["accent_purple"], "hover": "#a855f7"}
        }
        
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color=colors[style]["fg"],
            hover_color=colors[style]["hover"]
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
    
    # Calculator functions
    def add_to_expression(self, value):
        if self.current_expression == "0" or self.display_var.get() == "Error":
            self.current_expression = ""
        
        self.current_expression += str(value)
        self.update_display()
    
    def add_function(self, func):
        if self.current_expression == "0" or self.display_var.get() == "Error":
            self.current_expression = ""
        
        if func in ["sin", "cos", "tan", "asin", "acos", "atan"]:
            self.current_expression += f"math.{func}("
        elif func == "sqrt":
            self.current_expression += "math.sqrt("
        elif func == "log":
            self.current_expression += "math.log("
        elif func == "log10":
            self.current_expression += "math.log10("
        
        self.update_display()
    
    def add_hex_digit(self, digit):
        if self.current_base == "HEX":
            self.add_to_expression(digit)
    
    def update_display(self):
        display_text = self.current_expression.replace("*", "×").replace("/", "÷")
        display_text = display_text.replace("math.pi", "π").replace("math.e", "e")
        self.expression_display.configure(text=display_text)
        
        if len(display_text) > 15:
            display_text = "..." + display_text[-15:]
        self.display_var.set(display_text if display_text else "0")
    
    def clear(self):
        self.current_expression = ""
        self.display_var.set("0")
        self.expression_display.configure(text="")
    
    def clear_entry(self):
        self.current_expression = ""
        self.display_var.set("0")
    
    def backspace(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
        self.update_display()
    
    def toggle_sign(self):
        try:
            current = float(self.display_var.get())
            result = -current
            self.current_expression = str(result)
            self.display_var.set(str(result))
        except:
            pass
    
    def reciprocal(self):
        try:
            current = float(self.display_var.get())
            if current != 0:
                result = 1 / current
                self.current_expression = str(result)
                self.display_var.set(str(result))
        except:
            pass
    
    def factorial(self):
        try:
            current = int(float(self.display_var.get()))
            if current >= 0:
                result = math.factorial(current)
                self.current_expression = str(result)
                self.display_var.set(str(result))
        except:
            pass
    
    def calculate(self):
        try:
            if not self.current_expression:
                return
            
            expression = self.current_expression
            
            # Handle angle conversions for trig functions
            if self.angle_mode == "DEG":
                expression = expression.replace("math.sin(", "math.sin(math.radians(")
                expression = expression.replace("math.cos(", "math.cos(math.radians(")
                expression = expression.replace("math.tan(", "math.tan(math.radians(")
            elif self.angle_mode == "GRAD":
                expression = expression.replace("math.sin(", "math.sin(math.radians(")
                expression = expression.replace("math.cos(", "math.cos(math.radians(")
                expression = expression.replace("math.tan(", "math.tan(math.radians(")
                # Convert gradians to degrees first
                # This is simplified - you'd need more complex parsing
            
            # Handle missing parentheses
            open_parens = expression.count("(")
            close_parens = expression.count(")")
            missing_parens = open_parens - close_parens
            expression += ")" * missing_parens
            
            # Evaluate
            result = eval(expression)
            
            if result == float('inf') or result == float('-inf'):
                raise ZeroDivisionError
            
            # Format result
            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
                    result = f"{result:g}"
            
            # Add to history
            self.history.append(f"{self.current_expression} = {result}")
            if len(self.history) > 50:  # Keep last 50 calculations
                self.history.pop(0)
            
            self.current_expression = str(result)
            self.display_var.set(str(result))
            self.expression_display.configure(text="")
            
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by zero")
            self.current_expression = ""
        except:
            self.display_var.set("Error")
            self.current_expression = ""
    
    # Memory functions
    def memory_clear(self):
        self.memory = 0
        self.memory_indicator.configure(text="")
    
    def memory_recall(self):
        self.current_expression = str(self.memory)
        self.display_var.set(str(self.memory))
    
    def memory_add(self):
        try:
            current = float(self.display_var.get())
            self.memory += current
            self.memory_indicator.configure(text="M")
        except:
            pass
    
    def memory_subtract(self):
        try:
            current = float(self.display_var.get())
            self.memory -= current
            self.memory_indicator.configure(text="M")
        except:
            pass
    
    def memory_store(self):
        try:
            current = float(self.display_var.get())
            self.memory = current
            self.memory_indicator.configure(text="M")
        except:
            pass
    
    # Mode functions
    def set_angle_mode(self, mode):
        self.angle_mode = mode
        self.mode_label.configure(text=f"{self.current_mode} | {self.angle_mode}")
        # Update button colors
        self.switch_mode(self.current_mode)
    
    def set_base_mode(self, base):
        self.current_base = base
        # Update button colors and availability
        self.switch_mode(self.current_mode)
    
    # Date calculator
    def calculate_date_difference(self):
        try:
            date1_str = self.date1_entry.get()
            date2_str = self.date2_entry.get()
            
            date1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d")
            date2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d")
            
            diff = abs((date2 - date1).days)
            years = diff // 365
            months = (diff % 365) // 30
            days = (diff % 365) % 30
            
            result = f"Difference: {diff} days\n({years} years, {months} months, {days} days)"
            self.date_result.configure(text=result)
        except:
            self.date_result.configure(text="Invalid date format")
    
    # Unit converter
    def convert_units(self):
        try:
            value = float(self.conv_input.get())
            from_u = self.from_unit.get()
            to_u = self.to_unit.get()
            
            # Simple length conversion (you'd expand this)
            conversions = {
                "meter": 1,
                "kilometer": 1000,
                "centimeter": 0.01,
                "inch": 0.0254,
                "foot": 0.3048
            }
            
            if from_u in conversions and to_u in conversions:
                meters = value * conversions[from_u]
                result = meters / conversions[to_u]
                self.conv_result.configure(text=f"{value} {from_u} = {result:.6g} {to_u}")
            else:
                self.conv_result.configure(text="Conversion not available")
        except:
            self.conv_result.configure(text="Invalid input")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = AdvancedCalculator()
    calculator.run()
