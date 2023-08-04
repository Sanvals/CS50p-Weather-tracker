import argparse
import requests
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate


def main():
    # Parse the user input
    parser = argparse.ArgumentParser(description="Get IP and location")
    parser.add_argument("--ip", help="Type an IP address", type=str)
    parser.add_argument(
        "--city",
        help="Type a city, if the city has more than 2 worsd, use 'quotes'",
        type=str,
    )
    args = parser.parse_args()

    # If the user inputs an IP, fetch it and get a location
    if args.ip and args.city is None:
        ip = args.ip
        city = "-".join(get_city(ip).split(" "))
        print(f"Fetched: {ip}")
        print(f"Location: {city}")

    # If the user didn't input any location, fetch i
    elif args.city and args.ip is None:
        city = "-".join(args.city.split(" "))
        print(f"Location: {city}")

    else:
        # Else, fetch IP and location
        ip = get_ip()
        city = "-".join(get_city(ip).split(" "))
        print(f"Detected: {ip}")
        print(f"Fetched: {city}")

    # Send the url
    url = get_url(city)

    # Parse the data
    data = get_data(url)

    # Print it tabulated
    header = data[0].keys()
    rows = [x.values() for x in data]

    print(tabulate(rows, header, tablefmt="presto"))


def get_ip():
    """Get the IP from ipify"""
    ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    return ip


def get_city(ip):
    """Ghet the location from ipapi"""
    try:
        city = requests.get(f"https://ipapi.co/{ip}/json/").json()["city"]
        return city

    except KeyError:
        print("IP not valid")
        sys.exit(1)


def get_url(city):
    """Append the rest of the url to the chosen city"""
    url = "https://www.tiempo.com/" + city.lower() + ".htm"
    return url


def get_data(url):
    """Scraps forecast info from a eltiempo.com"""
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    # Extract days, weather and temperature
    forecast_data = []

    forecast_day = soup.find_all(class_="dia")

    for i, value in enumerate(forecast_day):
        # Format days
        day = value.find("span", class_="cuando")
        day = day.find("span").text
        day = format_day(day)

        # Format temperature
        temp = value.find("span", class_="temperatura")
        temp = format_temp(temp)

        # Format the weather
        weather = value.find("span", class_="prediccion")
        weather = weather.find("img", alt=True)["alt"]
        weather = format_weather(weather)

        # Make day, temp and weather into a dictionary
        state = {"day": day, "temp": temp, "meteo": weather}
        # Append it to the forecast_data list
        forecast_data.append(state)

    try:
        forecast_data[0]
        return forecast_data
    except IndexError:
        print("City not found")
        sys.exit(1)


def format_day(s):
    """Format the days into MM/DD format"""
    monthIndex = [
        "Ene",
        "Feb",
        "Mar",
        "Abr",
        "May",
        "Jun",
        "Jul",
        "Ago",
        "Sept",
        "Oct",
        "Nov",
        "Dic",
    ]

    day, month = s.split(" ")
    day = f"{int(day):02d}"
    month = f"{int(monthIndex.index(month) + 1):02d}"
    return f"{month}/{day}"


def format_temp(s):
    """Formats the temperature into XXº/XXºC format"""
    min = s.find("span", class_="minima").text
    max = s.find("span", class_="maxima").text
    return f"{min}/{max}C"


def format_weather(s):
    """Transforms the weather data into emoji"""
    if "Niebla" in s:
        day = "🌫️"
    elif "despejados" in s:
        day = "☀️"
    elif "cubiertos" in s:
        if "lluvias" in s:
            day = "🌧️"
        else:
            day = "🌦️"
    elif "nubosos" in s:
        if "lluvias" in s:
            day = "🌦️"
        else:
            day = "🌤️"
    else:
        return None

    return day


if __name__ == "__main__":
    main()
