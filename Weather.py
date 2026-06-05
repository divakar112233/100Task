import requests

api_key = "YOUR_API_KEY"

city = input("Enter city name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
data = response.json()

if data["cod"] == 200:
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]

    print("\nWeather Report")
    print("----------------")
    print("City:", city)
    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity, "%")
    print("Condition:", weather)
else:
    print("City not found!")