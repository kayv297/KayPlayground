import tkinter as tk
import pandas as pd
import requests
import matplotlib.pyplot as plt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from time import sleep
from tkinter import ttk
import csv
from datetime import datetime
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog


FOLDER_DESTINATION = r"C:\Users\Kha Vu\FoundOfPython\final_project"
FILE_DESTINATION = r"\CoinPrice.csv"
pd.set_option("display.float_format", lambda x: "%.2f" % x) #set 2 num after decimal point
table = None
table_frame = None
data = None
runtime_update_active = False

def api_runner():
    # Make API request to get crypto data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'50',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'e3c51909-132c-4b86-ba2d-98a559ed5a2e',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        error_label.config(text="Error: None")
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        error_label.config(text="Error: " + str(e))

    # Process the data and insert to CSV
    df = pd.json_normalize(data["data"])
    df["timestamp"] = pd.to_datetime("now")
    df["timestamp"] = df["timestamp"].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Save the data to a CSV file
    if not os.path.exists(FOLDER_DESTINATION+FILE_DESTINATION):
        df.to_csv("CoinPrice.csv", header = "column_names", float_format='%.2f')
    else:
        df.to_csv("CoinPrice.csv", mode = "a", header = False, float_format='%.2f')

# Get data and update the runtime label
def update_runtime_label():
    global runtime_seconds
    global runtime_update_active
    runtime_seconds = 0
    runtime_update_active = True
    while runtime_update_active:
        sleep(1)  # Wait for 1 second
        runtime_seconds += 1
        runtime_label.config(text=f"Runtime: {runtime_seconds} seconds")
        
def stop_runtime_update():
    global runtime_update_active
    runtime_update_active = False

def get_data():
    # Start the runtime update in a separate thread
    runtime_thread = threading.Thread(target=update_runtime_label)
    runtime_thread.start()

    for _ in range(5):
        api_runner()
        print("Ran")
        sleep(10)
    show_table()

    # Stop the runtime update thread after the task is done
    stop_runtime_update()
    show_table()

def parallel_get_data():
    data_thread = threading.Thread(target=get_data)
    data_thread.start()

# Show the table
def show_table():
    global data
    data = pd.read_csv('CoinPrice.csv', usecols=['name', 'symbol', 'quote.USD.price', 'quote.USD.percent_change_24h', 'timestamp'])
    global table
    global table_frame

    for widget in table_frame.winfo_children():
        widget.destroy()

    # Create a Treeview widget for the table within the table_frame
    table = ttk.Treeview(table_frame, columns=list(data.columns), show="headings")
    for column in data.columns:
        table.heading(column, text=column)
        table.column(column, width=100, anchor=tk.CENTER)

    # Insert data into the Treeview
    for _, row in data.iterrows():
        table.insert('', tk.END, values=list(row))

    # crollbar and associate it with the Treeview
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)

    # Position the Treeview and Scrollbar in the table_frame
    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    search_var.set('')
    search_label.grid(row=7, column=0, sticky='w')
    search_bar.grid(row=8, column=0, sticky='nsew', pady=(10, 0))  

# Top 10 by fluctuations
def top_10_by_fluc():
    global table, table_frame
    df = pd.read_csv('CoinPrice.csv')
    dfa = df.groupby("name", sort = False)[['quote.USD.percent_change_1h',
                                            'quote.USD.percent_change_24h',
                                            'quote.USD.percent_change_7d',
                                            'quote.USD.percent_change_30d',
                                            'quote.USD.percent_change_60d',
                                            'quote.USD.percent_change_90d']].mean()
    # Calculate the sum of squares of all numeric columns for each row
    dfa['sum_squares'] = dfa.apply(lambda row: sum(row**2), axis=1)
    top_10 = dfa.sort_values(by='sum_squares', ascending=False).head(10)
    top_10 = top_10.drop(columns='sum_squares').transpose()

    top_10 = top_10.iloc[::-1]
    
    fig, ax = plt.subplots()

    dfmatplot = top_10.reset_index()
    dfmatplot = dfmatplot.rename(columns={"index": "timeframe"})
    dfmatplot["timeframe"] = dfmatplot["timeframe"].str.lstrip("quote.USD.percent_change_")
    dfmatplot = dfmatplot.set_index("timeframe")
    dfmatplot.plot(figsize = (10,6), title = "Top 10 by Fluctuations", ax = ax)
    ax.set_xlabel("Timeframe")
    ax.set_ylabel("Percent Change")

    # Clear the frame (if there's anything in it)
    for widget in table_frame.winfo_children():
        widget.destroy()
    table = None
    # Create a canvas and embed the figure into table_frame
    canvas = FigureCanvasTkAgg(fig, master=table_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    search_label.grid_forget()
    search_bar.grid_forget()

# Top 10 by prices
def top_10_by_price():
    global table_frame, table
    df = pd.read_csv('CoinPrice.csv')
    dfa = df.groupby("name", sort=False)[['quote.USD.price']].mean()
    top_10 = dfa.sort_values(by='quote.USD.price', ascending=False).head(10)

    fig, ax = plt.subplots()

    # Plotting the bar chart
    top_10.plot(kind='bar', figsize=(10, 6), ax=ax, legend=False)
    ax.set_title("Top 10 Cryptocurrencies by Price")
    ax.set_xlabel("Cryptocurrency")
    ax.set_ylabel("Average Price (USD)")

    # Clear the frame (if there's anything in it)
    for widget in table_frame.winfo_children():
        widget.destroy()
    table = None
    # Create a canvas and embed the figure into table_frame
    canvas = FigureCanvasTkAgg(fig, master=table_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    search_label.grid_forget()
    search_bar.grid_forget()

# Function to be called when search price button is clicked
def plot_crypto_prices(symbol):
    # Filter the DataFrame for the given symbol
    global table_frame, table
    df = pd.read_csv('CoinPrice.csv')
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = df["timestamp"].dt.strftime('%Y-%m-%d')

    filtered_data = df[df['symbol'].str.lower() == symbol.lower()][['timestamp', 'quote.USD.price']]
    filtered_data = filtered_data.groupby('timestamp').mean().reset_index()
    filtered_data = filtered_data.rename(columns={"quote.USD.price": "price"})
    
    if filtered_data.empty:
        # If no data is found for the symbol, show an error message
        error_label.config(text=f"Error: No data for {symbol.upper()}")
        for widget in table_frame.winfo_children():
            widget.destroy()
        table = None
        return
    
    # Plotting
    fig, ax = plt.subplots()
    
    filtered_data.plot(x='timestamp', y='price', ax=ax, title=f"Price of {symbol.upper()} over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (USD)")
    
    # Clear the frame (if there's anything in it)
    for widget in table_frame.winfo_children():
        widget.destroy()
    table = None
    # Create a canvas and embed the figure into the Tkinter GUI within 'table_frame'
    canvas = FigureCanvasTkAgg(fig, master=table_frame) 
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    error_label.config(text=f"Error: None")


def on_search_price_clicked():
    # Create a dialog for input
    symbol = simpledialog.askstring("Input", "Enter the symbol to search for:",
                                    parent=root)
    if symbol:  # Ensure the user entered a symbol
        plot_crypto_prices(symbol)
        search_label.grid_forget()
        search_bar.grid_forget()

# Create GUI
root = tk.Tk()
root.title('Crypto API GUI')
root.geometry('1920x1080')

# Frame for the buttons
frame = tk.Frame(root)
frame.pack(side='left', anchor='nw', padx=20, pady=20)

get_data_button = tk.Button(frame, text='Get Data', command=parallel_get_data, width=20, height=2)
fluc_button = tk.Button(frame, text='Top Fluctuation', command=top_10_by_fluc, width=20, height=2)
show_table_button = tk.Button(frame, text='Show Table', command=show_table, width=20, height=2)
fluc_button = tk.Button(frame, text='Top Fluctuation', command=top_10_by_fluc, width=20, height=2)
price_button = tk.Button(frame, text='Top Price', command=top_10_by_price, width=20, height=2)
search_price = tk.Button(frame, text='Search Price', command=on_search_price_clicked, width=20, height=2)

    # Configure the grid layout within the frame
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)

    # Create a label with text to be placed above the buttons
header_label = tk.Label(frame, text="Crypto Dashboard", font=('Arial', 16))
header_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 20))

    # Adjust the placement of your buttons to the next row
get_data_button.grid(row=1, column=0, sticky='nsew')
show_table_button.grid(row=2, column=0, sticky='nsew')
fluc_button.grid(row=3, column=0, sticky='nsew')
price_button.grid(row=4, column=0, sticky='nsew')
search_price.grid(row=5, column=0, sticky='nsew')

# Frame for the table
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

# Break bar
break_bar = tk.Label(frame, text="", font=('Arial', 12))
break_bar.grid(row=6, column=0, sticky='w')

# Search bar
# Search label
search_label = tk.Label(frame, text="Search:", font=('Arial', 12))
search_label.grid(row=7, column=0, sticky='w')
    # Create the search bar Entry widget
search_var = tk.StringVar()
search_bar = tk.Entry(frame, textvariable=search_var)
search_bar.grid(row=8, column=0, sticky='nsew', pady=(10, 0))  # Place it in row 4, add some padding on top

    # Update the search function to hide non-matching rows
def search_table(*args):
    search_query = search_var.get().lower()  # Get the current text from search bar, convert to lowercase for case-insensitive search
    
    # Clear the table
    for child in table.get_children():
        table.delete(child)
    
    if search_query == "":
        # If search query is empty, repopulate the table with all items
        for _, row in data.iterrows():
            table.insert('', tk.END, values=list(row))
    else:
        # Repopulate the table with items that match the search query
        for _, row in data.iterrows():
            name = row['name'].lower()
            symbol = row['symbol'].lower()
            
            if search_query in name or search_query in symbol:
                table.insert('', 'end', values=list(row))

# Ensure the search_table function is called whenever the search_var changes
search_var.trace_add('write', search_table)

# Error label
error_label = tk.Label(root, text="Error: ", fg="red")
error_label.place(relx=0.0, rely=0.95, anchor='sw')

# Runtime label
runtime_label = tk.Label(root, text="Runtime:", fg="red")
runtime_label.place(relx=0.0, rely=1.0, anchor='sw')

search_label.grid_forget()
search_bar.grid_forget()
root.mainloop()