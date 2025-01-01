import requests  # importing the pip3 requests
from tkinter import *  # importing the GUI (Tkinter)

# Function to fetch weather data
def submit():
    user_input = entry.get()  # Gets the user input
    print(user_input)

    api_key = "bef13e08b11dec893970e1e3326b0c70"  # API key for the weather app 

    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}")
    
    if weather_data.json()['cod'] == '404': #if no city is found
        print("No City found")
        result_label.config(text="City not found. Please try again.", fg="red")
        temp_label.config(text="")
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = int(weather_data.json()['main']['temp'])

        print(f"The weather in {user_input} is: {weather}")
        print(f"The temperature in {user_input} is: {temp} °C")

        result_label.config(text=f"The weather in {user_input} is: {weather}")
        temp_label.config(text=f"The temperature in {user_input} is: {temp} °C", fg="black")


# Set up for the GUI window
window = Tk()  # Instantiate the window
window.geometry("420x420")
window.config(background='white')
window.title("Weather App")

# Create entry widget for user to input city
entry = Entry(window, font=('Arial', 14), width=20)
entry.pack(pady=10)

#Instructions
instruction_label = Label(window,text='Please enter the city',font =('Arial',18), fg = "#000000" )
instruction_label.pack(pady=15)

# The submit button
submit_button = Button(window, text="Submit", font=('Arial', 14), command=submit)
submit_button.pack()

# Label to display results
result_label = Label(window, text="", font=('Arial', 18), fg='#000000')
result_label.pack()

temp_label = Label(window, text="", font=('Arial', 18), fg='#000000')
temp_label.pack()

# Start the main loop
window.mainloop()



