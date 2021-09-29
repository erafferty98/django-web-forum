from django.test import TestCase
# First let us connect to the posts API and try to retrieve some data
# First import the requests package
import requests
# Then use the correct URL to retrieve data from the database
# Our database is empty, but still we can request to see the empty set
url = "http://10.61.64.79:8000/v1/posts/"
response = requests.get(url)

# Let us transform the response in JSON format
json_response = response.json()
print(json_response)

url = "http://10.61.64.79:8000/authentication/register/"

mary = {
            'username': 'mary',
            'password':'marymary1234'
        }

olga = {
            'username': 'olga',
            'password':'olgaolga1234'
        }

nestor = {
            'username': 'nestor',
            'password':'nestornestor1234'
        }

nick = {
            'username': 'nick',
            'password':'nicknick1234'
        }
    
mary_response = requests.post(url, data = mary)
mary_response = mary_response.json()
print(mary_response)

mary_token = mary_response['access_token']
print(mary_token)


olga_response = requests.post(url, data = olga)
olga_response = olga_response.json()
print(olga_response)

olga_token = olga_response['access_token']
print(olga_token)


nestor_response = requests.post(url, data = nestor)
nestor_response = nestor_response.json()
print(nestor_response)

nestor_token = nestor_response['access_token']
print(nestor_token)



nick_response = requests.post(url, data = nick)
nick_response = nick_response.json()
print(nick_response)

nick_token = nick_response['access_token']
print(nick_token)

