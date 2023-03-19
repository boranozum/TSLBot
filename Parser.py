import requests

class Parser:

    def __init__(self, base_url, params):
        self.base_url = base_url
        self.params = params
        self.headers = {
            "X-RapidAPI-Key": "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

    def get_data(self):
        response = requests.request("GET", self.base_url, headers=self.headers, params=self.params).json()
        return response['response']



