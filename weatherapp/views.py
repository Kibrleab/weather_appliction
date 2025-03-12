import requests
import datetime
from django.shortcuts import render
from django.contrib import messages

def home(request):
    city = request.POST.get('city', 'Addis Ababa')  # ✅ Get city safely

    # Weather API
    WEATHER_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=e16add4cbfbfe91c655a6011f74b2aab'
    PARAMS = {'units': 'metric'}

    # Google Image Search API
    API_KEY = 'AIzaSyAMjLq6H3ChcpjvdDOqBkAxc8uBPkkVr6E'
    SEARCH_ENGINE_ID = 'd6ec216825dc443ee'
    query = city + " 1920*1080"
    search_url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&imgSize=large'

    # Get weather data
    response = requests.get(WEATHER_URL, params=PARAMS)
    if response.status_code == 200:
        data = response.json()
    else:
        data = {}

    # Handle weather data
    if data.get("cod") != 200:
        messages.error(request, "Invalid city name. Showing default weather.")
        description = "Clear Sky"
        icon = "01d"
        temp = 25
        city = "Durame"
    else:
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

    # Get image data
    image_response = requests.get(search_url)
    if image_response.status_code == 200:
        search_items = image_response.json().get('items', [])
        image_url = search_items[0]['link'] if search_items else None
    else:
        image_url = None  # No image found

    # Render template
    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': datetime.date.today(),
        'city': city,
        'image_url': image_url
    })
