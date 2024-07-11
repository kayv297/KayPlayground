# Import the required libraries
import tkinter as tk

# Define the main application class
class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        # Initialize the string variable to display the result
        self.result_var = tk.StringVar()

        # Create the display widget
        self.display = tk.Entry(master, textvariable=self.result_var, justify='right', font=('Arial', 24))
        self.display.grid(row=0, column=0, columnspan=4, pady=10, padx=10, ipady=10, sticky='nsew')

        # Define the buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '+/-', '0', '.', '+',
        ]

        # Create and place the buttons in a grid
        row = 1
        col = 0
        for button in buttons:
            tk.Button(master, text=button, width=5, height=2, font=('Arial', 18),
                      command=lambda b=button: self.on_button_click(b)).grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        equal = tk.Button(master, text='=', width=5, height=2, font=('Arial', 18),
                          command=lambda: self.on_button_click('='))
        equal.grid(row=row, column=3)
        clear = tk.Button(master, text='C', width=5, height=2, font=('Arial', 18),
                          command=lambda: self.on_button_click('C'))
        clear.grid(row=row, column=0)
        

    def on_button_click(self, button):
        if button == '=': #eval the expression
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except Exception as e:
                self.result_var.set("Error")
        elif button == 'C': #clear
            self.result_var.set("")
        elif button == '+/-': #negate
            self.result_var.set(str(-1 * float(self.result_var.get())))
        elif button == '0' and self.result_var.get() == '': #no leading 0
            pass
        else: #update screen
            self.result_var.set(self.result_var.get() + button)

# Create the main window (instance of Tk)
root = tk.Tk()
app = CalculatorApp(root)

# Start the application
root.mainloop()