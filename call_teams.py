import requests

url = "https://v3.football.api-sports.io/teams?country ='England'&season=2022&league"
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a86d420d0d8840c8e722e16cf9742f7b"
    }

data = requests.request("GET", url, headers=headers).json()
print(data)