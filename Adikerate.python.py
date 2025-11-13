import tkinter as tk
from tkinter import messagebox, simpledialog

#Comment

class AdikeKeniApp:
    # Define default placeholder texts as constants
    SEASON_PLACEHOLDER = "Enter season"
    WEIGHT_PLACEHOLDER = "Enter weight (kg)"
    CONVERSION_RATIO = 12  # Fixed conversion based on 100kg = 12kg

    def __init__(self, root):
        self.root = root
        self.root.title("YASHU APP")
        self.root.geometry("1000x600")
        self.seasonal_weights = []

        # GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        tk.Label(self.root, text="Adike Keni App", font=("Arial", 16)).pack(pady=10)

        # Author Label
        tk.Label(self.root, text="", font=("Arial", 10, "italic")).pack(pady=5)

        # Input Section
        tk.Label(self.root, text="Add Seasonal Weight", font=("Arial", 12)).pack(pady=5)
        self.season_entry = tk.Entry(self.root, width=30)
        self.season_entry.insert(0, self.SEASON_PLACEHOLDER)
        self.season_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, self.SEASON_PLACEHOLDER))
        self.season_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.SEASON_PLACEHOLDER))
        self.season_entry.pack(pady=5)

        self.weight_entry = tk.Entry(self.root, width=30)
        self.weight_entry.insert(0, self.WEIGHT_PLACEHOLDER)
        self.weight_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, self.WEIGHT_PLACEHOLDER))
        self.weight_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.WEIGHT_PLACEHOLDER))
        self.weight_entry.pack(pady=5)

        tk.Button(self.root, text="Add Weight", command=self.add_season_weight).pack(pady=10)
        tk.Button(self.root, text="Clear All", command=self.clear_all_seasonal_weights, bg="lightblue").pack(pady=5)

        # Calculation Section
        tk.Label(self.root, text="Bill Calculation", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.root, text="Market Price Mode", command=self.calculate_market_price).pack(pady=5)
        tk.Button(self.root, text="Converted Weight Mode", command=self.calculate_converted_weight).pack(pady=5)
        tk.Button(self.root, text="Custom Calculation", command=self.custom_calculation).pack(pady=5)
        tk.Button(self.root, text="Crop Final Rate Calculator", command=self.crop_final_rate_calculator).pack(pady=5)

        # Summary Section
        tk.Button(self.root, text="View Summary", command=self.display_summary).pack(pady=10)

        # Restart & Exit Buttons
        tk.Button(self.root, text="Restart", command=self.restart_app, bg="orange", fg="white").pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.confirm_exit, bg="red", fg="white").pack(pady=5)

    def clear_placeholder(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="black")

    def add_placeholder(self, event, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg="grey")

    def add_season_weight(self):
        season = self.season_entry.get().strip()
        if season == self.SEASON_PLACEHOLDER or not season:
            messagebox.showerror("Error", "Season name cannot be empty.")
            return
        try:
            weight_text = self.weight_entry.get().strip()
            if weight_text == self.WEIGHT_PLACEHOLDER or not weight_text:
                raise ValueError
            weight = float(weight_text)
            if weight <= 0:
                messagebox.showerror("Error", "Weight must be greater than zero.")
                return
            formatted_season = f"Season: {season}"  # Add "Season:" before the user input
            if any(item['season'].lower() == formatted_season.lower() for item in self.seasonal_weights):
                messagebox.showerror("Error", f"{formatted_season} already exists.")
                return
            self.seasonal_weights.append({"season": formatted_season, "weight": weight})
            messagebox.showinfo("Success", f"Added {weight} kg for {formatted_season}.")
            self.season_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
            self.add_placeholder(tk.Event(), self.SEASON_PLACEHOLDER)
            self.add_placeholder(tk.Event(), self.WEIGHT_PLACEHOLDER)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid weight.")

    def clear_all_seasonal_weights(self):
        self.seasonal_weights.clear()
        messagebox.showinfo("Cleared", "All seasonal weight data has been cleared.")

    def calculate_total_weight(self):
        return sum(item['weight'] for item in self.seasonal_weights)

    def calculate_market_price(self):
        if not self.seasonal_weights:
            messagebox.showerror("Error", "No seasonal weights added.")
            return
        try:
            price_per_kg = float(simpledialog.askstring("Market Price", "Enter market price per kg:"))
            if price_per_kg <= 0:
                raise ValueError
            total_weight = self.calculate_total_weight()
            total_bill = total_weight * price_per_kg
            messagebox.showinfo("Market Price Mode", f"Total Bill: ₹{total_bill:.2f}")
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter a valid price.")

    def calculate_converted_weight(self):
        if not self.seasonal_weights:
            messagebox.showerror("Error", "No seasonal weights added.")
            return
        try:
            conversion_factor = float(simpledialog.askstring("Conversion Factor", "Enter conversion factor (e.g., 12 for 100kg to 12kg):"))
            if conversion_factor <= 0:
                raise ValueError
            price_per_kg = float(simpledialog.askstring("Market Price", "Enter market price per kg:"))
            if price_per_kg <= 0:
                raise ValueError
            total_weight = self.calculate_total_weight()
            converted_weight = total_weight * (conversion_factor / 100)
            total_bill = converted_weight * price_per_kg
            messagebox.showinfo("Converted Weight Mode", f"Total Bill: ₹{total_bill:.2f}")
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter valid inputs.")

    def custom_calculation(self):
        try:
            custom_weight = float(simpledialog.askstring("Custom Weight", "Enter custom weight (kg):"))
            if custom_weight <= 0:
                raise ValueError
            custom_price = float(simpledialog.askstring("Custom Price", "Enter custom price per kg:"))
            if custom_price <= 0:
                raise ValueError
            total_bill = custom_weight * custom_price
            messagebox.showinfo("Custom Calculation", f"Total Bill: ₹{total_bill:.2f}")
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter valid inputs.")

    def crop_final_rate_calculator(self):
        if not self.seasonal_weights:
            messagebox.showerror("Error", "No seasonal weights added.")
            return
        try:
            rate_per_kg = float(simpledialog.askstring("Rate per kg", "Enter rate per kg:"))
            if rate_per_kg <= 0:
                raise ValueError
            total_weight = self.calculate_total_weight()
            converted_weight = total_weight * (self.CONVERSION_RATIO / 100)
            total_bill = converted_weight * rate_per_kg
            messagebox.showinfo("Crop Final Rate Calculator", f"Total Bill: ₹{total_bill:.2f}\nConverted Weight: {converted_weight:.2f} kg")
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter a valid rate.")

    def display_summary(self):
        if not self.seasonal_weights:
            messagebox.showerror("Error", "No seasonal weights added.")
            return
        summary = "Seasonal Weights Summary:\n"
        for item in self.seasonal_weights:
            summary += f"{item['season']}, Weight: {item['weight']} kg\n"
        messagebox.showinfo("Summary", summary)


if __name__ == "__main__":
    root = tk.Tk()
    app = AdikeKeniApp(root)
    root.mainloop()
