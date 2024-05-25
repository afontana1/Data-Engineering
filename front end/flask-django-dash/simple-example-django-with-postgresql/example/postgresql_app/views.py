from django.http import JsonResponse
from .models import Joke
import requests
import datetime

def index(request):
  api_endpoint = "https://api.chucknorris.io/jokes/random"
  response = requests.get(api_endpoint)
  response.raise_for_status()
  jsonResponse = response.json()
  newJoke = Joke(content=jsonResponse['value'],added_at=datetime.datetime.now())
  newJoke.save()
  response_data = {}

  response_data['jokes'] = [{
    'value': j.content,
    'addedAt': j.added_at
  } for j in Joke.objects.order_by('-added_at')]

  return JsonResponse(response_data)