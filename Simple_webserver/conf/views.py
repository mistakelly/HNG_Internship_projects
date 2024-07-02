# HELP ME GOD.
# STAGE 1 HNG INTERNSHIP
from django.http import HttpRequest, JsonResponse
from ipware import get_client_ip
import requests
from django.conf import settings


def simpleserver(request: HttpRequest):
    # get the client name
    client_name = request.GET.get("visitor_name", "unknown")

    # access users ip local ip_address, if application is behin d a proxy, or loadbalancer.
    client_ip = get_client_ip(request)[0]

    # get the client public ip address, using geojs api, when i tried getting the users information using the local ipaddress, geojs api returned some invalid response, so i had to use the public ip address.
    client_public_ip = requests.get(f"https://get.geojs.io/v1/ip.json")

    response = requests.get(
        f"https://get.geojs.io/v1/ip/geo/{client_public_ip.json()['ip']}.json"
    )


    client_city = response.json()["city"]

    # openwhethermap api conf.
    # get client's city whether information is available using openwhois api
    weather_api_key = settings.OPENWEATHER_API_KEY

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = client_city
    API_KEY = weather_api_key

    whether_api_url = f"{BASE_URL}q={CITY}&appid={API_KEY}"

    weather_response = requests.get(whether_api_url).json()

    client_city_tmp = weather_response["main"]["temp"]

    # return a response.
    print()
    return JsonResponse(
        {
            "client_ip": client_ip,
            "location": client_city,
            "greeting": f"Hello, {client_name}!, the temperature is {str(client_city_tmp).split('.')[0]} degrees Celcius in {client_city}",
        }, json_dumps_params={"indent": 4}
    )
