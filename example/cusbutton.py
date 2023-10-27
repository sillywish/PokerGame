import tkinter as tk

class CustomButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=tk.FLAT,  # Remove button relief
            bd=0,  # Remove border
            highlightthickness=0,  # Remove highlight
            padx=10,  # Add horizontal padding
            pady=5,  # Add vertical padding
            font=("Arial", 12),  # Set font
            foreground="white",  # Text color
            background="orange",  # Background color
        )
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(background="lightblue")  # Change color on hover

    def on_leave(self, event):
        self.config(background="green")  # Restore original color

# Create the main window
root = tk.Tk()
root.title("Custom Button Example")

# Create a custom button
custom_button = CustomButton(root, text="Custom Button")
custom_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()