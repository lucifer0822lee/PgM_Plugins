import json
import datetime
from requests import get
from pagermaid import version
from pagermaid.listener import listener
from pagermaid.utils import obtain_message, alias_command

icons = {
    "01d": "π",
    "01n": "π",
    "02d": "βοΈ",
    "02n": "βοΈ",
    "03d": "βοΈ",
    "03n": "βοΈ",
    "04d": "βοΈ",
    "04n": "βοΈ",
    "09d": "π§",
    "09n": "π§",
    "10d": "π¦",
    "10n": "π¦",
    "11d": "π©",
    "11n": "π©",
    "13d": "π¨",
    "13n": "π¨",
    "50d": "π«",
    "50n": "π«",
}


def timestamp_to_time(timestamp, timeZoneShift):
    timeArray = datetime.datetime.utcfromtimestamp(timestamp) + datetime.timedelta(seconds=timeZoneShift)
    return timeArray.strftime("%H:%M")


def calcWindDirection(windDirection):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(windDirection / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


@listener(is_plugin=True, outgoing=True, command=alias_command("weather"),
          description="ζ₯θ―’ε€©ζ°",
          parameters="<εεΈ>")
async def weather(context):
    await context.edit("θ·εδΈ­ . . .")
    try:
        message = await obtain_message(context)
    except ValueError:
        await context.edit("εΊιδΊεεε ~ ζ ζηεζ°γ")
        return
    try:
        req = get(
            "http://api.openweathermap.org/data/2.5/weather?appid=973e8a21e358ee9d30b47528b43a8746&units=metric&lang"
            "=zh_cn&q=" + message)
        if req.status_code == 200:
            data = json.loads(req.text)
            cityName = "{}, {}".format(data["name"], data["sys"]["country"])
            timeZoneShift = data["timezone"]
            temp_Max = round(data["main"]["temp_max"], 2)
            temp_Min = round(data["main"]["temp_min"], 2)
            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            windSpeed = data["wind"]["speed"]
            windDirection = calcWindDirection(data["wind"]["deg"])
            sunriseTimeunix = data["sys"]["sunrise"]
            sunriseTime = timestamp_to_time(sunriseTimeunix, timeZoneShift)
            sunsetTimeunix = data["sys"]["sunset"]
            sunsetTime = timestamp_to_time(sunsetTimeunix, timeZoneShift)
            fellsTemp = data["main"]["feels_like"]
            tempInC = round(data["main"]["temp"], 2)
            tempInF = round((1.8 * tempInC) + 32, 2)
            icon = data["weather"][0]["icon"]
            desc = data["weather"][0]["description"]
            res = "{} {}{} π¨{} {}m/s\nε€§ζ°π‘ {}β ({}β) π¦ {}% \nδ½ζπ‘ {}β\nζ°ε {}hpa\nπ{} π{} ".format(
                cityName, icons[icon], desc, windDirection, windSpeed, tempInC, tempInF, humidity, fellsTemp, pressure,
                sunriseTime, sunsetTime
            )
            await context.edit(res)
        if req.status_code == 404:
            await context.edit("εΊιδΊεεε ~ ζ ζηεεΈεοΌθ―·δ½Ώη¨ζΌι³θΎε₯ ~ ")
            return
    except Exception:
        await context.edit("εΊιδΊεεε ~ ζ ζ³θ?Ώι?ε° openweathermap.org γ")
