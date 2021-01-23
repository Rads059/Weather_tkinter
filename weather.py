import tkinter, requests
from tkinter import BOTH, IntVar
from PIL import ImageTk, Image
from io import BytesIO

main = tkinter.Tk()
main.title("Weather Forecast Software")

main.tk.call('wm', 'iconphoto', main._w, tkinter.PhotoImage(file='w.png'))

# main.iconbitmap('weather.XBM')
main.geometry('400x400')
main.resizable(0, 0)

# Define fonts and colors
sky_color = "#76c3ef"
grass_color = "#aad207"
output_color = "#dcf0fb"  # "#ecf2ae" #
input_color =  "#dcf0fb"         # "#ecf2ae"
large_font = ('Times New Roman', 14)
small_font = ('Times New Roman', 10)


# Defining functions


def search():
    global response
    # getting api response
    url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = '9de1b4068d42416de364a731336d3fa4'  # '6da92ea5e09090fa9c8a08e08eb30284'
    # Search by the appropriate query, either city name or zip
    if search_method.get() == 1:
        querystring = {"q": city_entry.get(), 'appid': api_key, 'units': 'metric'}
    elif search_method.get() == 2:
        querystring = {"zip": city_entry.get(), 'appid': api_key, 'units': 'metric'}
    # Call API
    response = requests.request("GET", url, params=querystring)
    response = response.json()

    weather()
    icon()


def weather():
    city_name = response['name']
    city_lat = str(response['coord']['lat'])
    city_lon = str(response['coord']['lon'])
    main_weather = response['weather'][0]['main']
    description = response['weather'][0]['description']
    temp = str(response['main']['temp'])
    feels_like = str(response['main']['feels_like'])
    temp_min = str(response['main']['temp_min'])
    temp_max = str(response['main']['temp_max'])
    humidity = str(response['main']['humidity'])

    # Update output lables
    city_info_label.config(text=city_name + "(" + city_lat + ", " + city_lon + ")",
                           font=large_font, bg=output_color)
    weather_label.config(text="Weather: " + main_weather + ", " + description,
                         font=small_font, bg=output_color)
    temp_label.config(text='Temperature: ' + temp + " C", font=small_font,
                      bg=output_color)
    feels_label.config(text="Feels Like: " + feels_like + " C", font=small_font,
                       bg=output_color)
    temp_min_label.config(text="Min Temperature: " + temp_min + " C", font=small_font,
                          bg=output_color)
    temp_max_label.config(text="Max Temperature: " + temp_max + " C", font=small_font,
                          bg=output_color)
    humidity_label.config(text="Humidity: " + humidity, font=small_font, bg=output_color)


def icon():
    global img
    icon_id = response['weather'][0]['icon']
    url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_id)
    icon_response = requests.get(url, stream=True)
    img_data = icon_response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    # Update label
    photo_label.config(image=img)


# Create Frames
sky_frame = tkinter.Frame(main, bg=sky_color, height=250)
grass_frame = tkinter.Frame(main, bg=grass_color)
sky_frame.pack(fill=BOTH, expand=True)
grass_frame.pack(fill=BOTH, expand=True)
output_frame = tkinter.LabelFrame(sky_frame, bg=output_color, width=325, height=225)
input_frame = tkinter.LabelFrame(grass_frame, bg=input_color, width=325)
output_frame.pack(pady=30)
output_frame.pack_propagate(0)
input_frame.pack(pady=15)

# Output frame layout
city_info_label = tkinter.Label(output_frame, bg=output_color)
weather_label = tkinter.Label(output_frame, bg=output_color)
temp_label = tkinter.Label(output_frame, bg=output_color)
feels_label = tkinter.Label(output_frame, bg=output_color)
temp_min_label = tkinter.Label(output_frame, bg=output_color)
temp_max_label = tkinter.Label(output_frame, bg=output_color)
humidity_label = tkinter.Label(output_frame, bg=output_color)
photo_label = tkinter.Label(output_frame, bg=output_color)
city_info_label.pack(pady=8)
weather_label.pack()
temp_label.pack()
feels_label.pack()
temp_min_label.pack()
temp_max_label.pack()
humidity_label.pack()
photo_label.pack(pady=8)

# Input frame layout
# Create input frame buttson and entry
city_entry = tkinter.Entry(input_frame, width=20, font=large_font)
submit_button = tkinter.Button(input_frame, text='Submit', font=large_font, bg=input_color, command=search)

search_method = IntVar()
search_method.set(1)
search_city = tkinter.Radiobutton(input_frame, text='Search by city name',
                                  variable=search_method, value=1, font=small_font, bg=input_color)
search_zip = tkinter.Radiobutton(input_frame, text="Search by zipcode",
                                 variable=search_method, value=2, font=small_font, bg=input_color)
city_entry.grid(row=0, column=0, padx=10, pady=(10, 0))
submit_button.grid(row=0, column=1, padx=8, pady=(10, 0))
search_city.grid(row=1, column=0, pady=5)
search_zip.grid(row=1, column=1, padx=5, pady=2)

main.mainloop()
