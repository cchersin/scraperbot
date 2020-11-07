from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def scrap(request):
  url = request.GET.get('url')
  token = request.GET.get('token')
  chat_id = request.GET.get('chat_id')
    
  lastReaded = lastReaded.objects.first()
  if lastReaded == nil:
      lastReaded = LastReaded(idx=1627)

  r =requests.get(url + '/index.php?page=documenti#1')
  text=r.text
  start=text.find('documenti.data = ')
  text=text[start+17:]
  end=text.find(']];')
  text=text[0:end+2]

  items = json.loads(text)
  items = items[::-1]
    
  count = 0

  for item in items:
    if item[6][0] == 'CIRCOLARI':
      data=item[1]
      itemIdx=int(item[10])
      if itemIdx > lastReaded.idx:
        msg=data + ' ' + item[4] + ' ' + url + '/' + item[5]
        r =requests.get('https://api.telegram.org/' + token + '/sendMessage?chat_id=' + chat_id + '&text=' + msg)
        lastReaded.idx=itemIdx
        count = count + 1
        
  lastReaded.save()
        
  return render(request, "scrap.html", { "count": count })

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
