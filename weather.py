# Import necessary libraries
import tkinter as tk
from tkinter import messagebox
import requests

# Define the function to fetch weather data
def get_weather():
    city = city_entry.get()
    api_key = "f6c558289d22ba5c8f3f49696ed75633"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data["cod"] == 200:
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        conditions = weather_data["weather"][0]["description"]
        temperature_label.config(text=f"Temperature: {temperature} °C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        conditions_label.config(text=f"Conditions: {conditions}")
    else:
        messagebox.showerror("Error", "City not found. Please try again.")

# Set up the GUI
root = tk.Tk()
root.title("Weather App")

# Create widgets
city_entry_label = tk.Label(root, text="Enter city name:")
city_entry = tk.Entry(root)
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
temperature_label = tk.Label(root, text="Temperature: ")
humidity_label = tk.Label(root, text="Humidity: ")
conditions_label = tk.Label(root, text="Conditions: ")

# Place widgets on the window
city_entry_label.grid(row=0, column=0, padx=10, pady=10)
city_entry.grid(row=0, column=1, padx=10, pady=10)
get_weather_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
temperature_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
humidity_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
conditions_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()